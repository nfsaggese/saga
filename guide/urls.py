from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^business/', views.business),
    url(r'^create-guide/$', views.create_guide),
    url(r'^create-address/$', views.create_address),
    url(r'^get-requirements-calendar/$', views.get_requirements_calendar)
    # url(r'^create-shift/$', views.create_shift),
]
