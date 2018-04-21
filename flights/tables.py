import django_tables2 as tables
from .models import Flight, Customer
from django_tables2.utils import A  # alias for Accessor
from .views import *


class FlightTable(tables.Table):
    edit = tables.LinkColumn('flights_detail', args=[A('pk')], orderable=False, empty_values=())

    class Meta:
        model = Flight
        template_name = 'django_tables2/bootstrap.html'


