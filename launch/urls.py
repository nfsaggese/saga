from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add-guide/', views.add_guide),
    url(r'^contact/$', views.contact),
]