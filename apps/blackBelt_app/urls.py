from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index), 
    url(r'^register$', views.register), 
    url(r'^login$', views.login), 
    url(r'^logout$', views.logout), 
    url(r'^home$', views.home),
    url(r'^addTrip$', views.addTrip),
    url(r'^createTrip$', views.createTrip),
    url(r'^tripInfo/(?P<kittycatlicklick>\d+)$', views.tripInfo),
    url(r'^joinTrip/(?P<kittysaurus>\d+)$', views.joinTrip),
    url(r'^remove/(?P<id>\d+)$', views.remove),
]