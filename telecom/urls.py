from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^call-guide/', views.call_guide, name='call-guide'),
    url(r'^connect-guide/', views.connect_guide, name='connect-guide'),
    url(r'^guide-accept-sound/', views.guide_accept_sound, name='guide-accept-sound'),
    url(r'^connect-guide-result/', views.connect_guide_result, name="connect-guide-result")
]