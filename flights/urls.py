from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.passengers_list, name='passengers_list'),
    url(r'^$', views.FilteredFlightListView.as_view(), name='flights_list'),
    url('flight/(\d+)/', views.flights_detail, name='flights_detail')
    # url(r'^airport/(?P<pk>\w+)/$', views.airports_list, name='airports_list'),
    # url('^flight/(?P<pk>\d+)/$', views.flights_detail, name='flight_detail')
]