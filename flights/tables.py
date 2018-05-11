import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from .views import *


class FlightTable(tables.Table):
    Choose = tables.LinkColumn('flights_detail', text='Choose', args=[A('pk')], orderable=False, empty_values=())

    class Meta:
        model = Flight
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('ticketsPurchased', 'id')


