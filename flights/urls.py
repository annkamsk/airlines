from django.conf.urls import url
from django.urls import re_path, include
from . import views
from . import models
from . import tables
from . import filters

urlpatterns = [
    url('flight/(\d+)/', views.flights_detail, name='flights_detail'),
    re_path(r'^auth/', include('django.contrib.auth.urls')),
    # url(r'^$', views.FilteredSingleTableView.as_view(
    #         model=models.Flight,
    #         table_class=tables.FlightTable,
    #         template_name='flights/flights_list.html',
    #         filter_class=filters.FlightFilter,
    #     ), name='flights_list'),
    url(r'^$', views.flights_list, name='flights_list')
]