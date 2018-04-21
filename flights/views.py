from django.shortcuts import render
from .models import Passenger, Flight, Airport, Airplane, Customer
from .tables import FlightTable
from .filters import FlightFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import RequestConfig


def passengers_list(request):
        passengers = Passenger.objects.all().order_by('surname')
        return render(request, 'flights/passengers_list.html', {'passengers': passengers})



def flights_list(request):
    table = FlightTable(Flight.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'flights/flights_list.html', {'table': FilteredFlightListView})


def flights_detail(request, pk):
    flight = Flight.objects.get(pk=pk)
    return render(request, 'flights/flights_detail.html', {'flight': flight})


class FilteredFlightListView(SingleTableMixin, FilterView):
    table_class = FlightTable
    model = Flight
    template_name = 'flights/flights_list.html'
    ordering = ['startingTime']
    filterset_class = FlightFilter



def airports_list(request):
    airports = Airport.objects.all().order_by('name')
    return render(request, 'flights/airports_list.html', {'airports': airports})