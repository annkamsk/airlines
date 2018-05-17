from django.conf.urls import url
from django.urls import re_path, include
from . import views
from . import models
from . import tables
from . import filters

urlpatterns = [
    url('flight/(\d+)/', views.flights_detail, name='flights_detail'),
    re_path(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^$', views.flights_list, name='flights_list')
]