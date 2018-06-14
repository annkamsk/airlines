from django.conf.urls import url
from django.urls import re_path, include
from . import views

urlpatterns = [
    url('flight/(\d+)/', views.flights_detail, name='flights_detail'),
    re_path(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^$', views.flights_list, name='flights_list'),
    url(r'^$', views.api_root),
    url(r'^crews/$', views.CrewList.as_view()),
    url(r'^flights/$', views.FlightList.as_view()),
    url(r'^assign-crew/$', views.assign_crew),
    url(r'^user-authenticate/$', views.user_authenticate),
]
