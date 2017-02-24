from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.main),
    url(r'^validateit$', views.validate),
    url(r'^travels$', views.travels),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^posttrip$', views.posttrip),
    url(r'^join/(?P<id>\d+)', views.join),
    url(r'^travels/destination/(?P<tripid>\d+)', views.destination),
]
