from guide import models
from datetime import datetime
#get events on date range
from scheduling import models as scheduling_models
from customer import models as customer_models
from scheduling.helpers import get_events
from dateutil.parser import parse as date_parse
from guide import serializers
from scheduling import serializers as scheduling_serializers
from django.forms.models import model_to_dict

class Availability_Schedule:
    def __init__(self, event, capacity):
        self.event = event
        self.capacity = capacity

class Choice_Requirement:
    def __init__(self, choices, req):
        self.req = req
        self.choices = choices

class Choice:
    def __init__(self, brands, choice):
        self.brands = brands
        self.choice = choice # holds

class Brand:
    def __init__(self,resource, items):
        self.resource = resource
        self.items = items
class Requirement(object):
    def __init__(self,req,pool):
        self.req = req
        self.pool = pool
class Item(object):
    def updateScheduled(self,update):
        self.scheduled = update
    def __init__(self, item, scheduled):
        self.item = item
        self.scheduled = scheduled#calendar scheduled
class Calendar(object):
    def add_event(self,event):
        self.calendar.append(event)
    def __init__(self,item):
        self.item = item
        self.calendar = []
# class Guide_Requirement_Inventory:
#     def __init__(self, req, available):
#         self.req = req
#         self.guides = available #pool of available guide_models
class Guide_Equipment_Requirement_Inventory:
    def __init__(self, req, items):
        self.req = req
        self.items = items


# class Event:
#     def __init__(self, start, end):
#         self.start = start
#         self.end = end

#Gather Requirements


def create_guide_requirement_calendar(experience,window_start,window_end):
    # print experience
    guide_reqs = models.Guide_Requirement.objects.filter(experience_id=experience)
    # print "Guide_Requirements"
    # print guide_reqs
    events = get_events.get_events(window_start,window_end)
    # print "These events"
    # print events
    reqs = []
    for req in guide_reqs:#for each requirement of guide_models
        pool = []
        # print req.pool

        for g in req.pool.all():
            print model_to_dict(g)
            unavailable = []
            for e in events:
                if len(scheduling_models.Attendee.objects.filter(event=e).filter(actor=g.actor)) >= 1:
                    unavailable.append(e)
            pool.append({
                "guide": serializers.Guide_Serializer(g).data,
                "calendar":scheduling_serializers.Event_Serializer(unavailable, many=True).data
            })
        # s = model_to_dict(req)
        # s["pool"] = serializers.Guide_Serializer(req.pool.all())
        # s = serializers.Guide_Requirement_Serializer(req)
        reqs.append({
            "requirement": serializers.Guide_Requirement_Serializer(req,).data,
            "pool": pool
        })
    return reqs

def get_requirements_calendar(experience,window_start,window_end):#gathers all requirements
    window_start = date_parse(window_start)
    # print window_start
    window_end= date_parse(window_end)
    # print window_end
    reqs = {"Guides":create_guide_requirement_calendar(experience,window_start,window_end)}
    return reqs


def get_guide_equipment_requirements(experience):
    equip = models.Guide_Equipment_Requirement.filter(experience=experience)
    reqs = []
    for req in equip:
        items = []
        for resource in req.pool:
            prefs = models.Guide_Equip_Preference(resource=resource)
            for item in prefs.pool:
                items.append(Item(item,0))
        reqs.append(Guide_Requirement_Inventory(req,items))
    return reqs

def get_resource_requirements(experience):#gets guide reqs in array, with guides attached in object, each unique so no issue
    res = models.Resource_Requirement.filter(experience=experience)
    reqs = []
    for req in res:#requirement in all requirements
        s = []
        for r in req.pool:# r is resource
            t=[]
            ind = models.Ind_Resource.filter(resource=resource)
            for i in ind:
                t.append(Item(i,0))
            s.append(Brand(r,t))#needs to be reevaluated per event
        reqs.append(Choice(s,req))#TODO make choice and other classes more general, this is a appending a resource requirememnt to a list of overall resource requirements which is returned
    return reqs

def get_resource_choice_requirements(experience):#do once...maybe cache this?...still needs to be once per session ish
    resource_choice_reqs = models.Resource_Choice_Requirement.filter(experience=experience)
    choice_requirements = []
    for req in resource_choice_reqs:
        choices = models.Resource_Choice_Pool.filter(resource_choice_requirement=req)
        choiceObjects = []
        for choice in choices:#choices
            brands = []
            for resource in choice.pool:#resource corresponds to a choice
                pieces = models.Ind_Resource.filter(resource=resource)#individual resources, belongs to resource
                items = []
                for item in pieces:
                    items.append(Item(item,0))#only shows base reqs..now need to get live availability from calendar
                brands.append(Brand(resource,items))#append brand to brands objects list
            choiceObjects.append(Choice(brands,choice))#add choice object to choice object list
        choice_requirements.append(Choice_Requirement(req,choiceObjects))# add choice rquirement to choice requirement list
    return choice_requirements
def get_specific_resource_requirements(experience):#list of requirement objects with applicable items underneath and inventory levels
    reqs = models.Specific_Resource_Requirement.filter(experience=experience)
    s = []
    for req in reqs:
        c = []
        for i in req.pool:
            c.append(Item(i,0))
        s.append(Brand(req,c))
#Tours
def get_tour_schedule(experience,window_start,window_end):
    tour_schedules = models.Tour_Schedule.filter(tour=experience)
    events = []
    for sched in tour_schedules:#get all timetable events
        events.extend(sched.timetable.filter(start__gte=window_start).filter(end__lte=window_end))
    # datetime.datetime.now() + datetime.timedelta(3*365)
    return events
#Courses
def get_course_schedule(experience,window_end):
    courses = models.Course_Session(course = experience)
    events = []
    for sched in courses:
        events.append(sched.session.filter(start__gte=window_start).filter(end__lte=window_end))
    return events

def get_general_availability_tour(tour, window_start, window_end):#get number of participants, non private
    events = get_tour_schedule(tour, window_start, window_end)
    availability = []
    for event in events:
        purchase = customer_models.Tour_Purchase.filter(event=event)
        capacity = tour.max_capacity - purchase.num_attendees
        private = purchase.pricepoint.private
        if(private):
            capacity = 0
        availability.append(Availaibility_Schedule(event,capacity))
    #find reqs...

#Shifts
def get_shift_guide_requirements(shift):#get
    shift_reqs = models.Shift_Guide_Requirement.filter(shift=shift)
    reqs = []
    for req in shift_reqs:
        reqs.append(Guide_Requirement_Inventory(req,req.pool))
    return reqs

# def get_shift_resource_requirements(shift):
#     shift_reqs = models.Shift_Guide_Requirement.filter(shift=shift)
#     reqs = []
#     for req in shift_reqs:
#         reqs.append(Guide_Requirement_Inventory(req,req.pool))
#     return reqs
