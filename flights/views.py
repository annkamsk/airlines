from django.shortcuts import render
from .models import Passenger, Flight
from .forms import PassengerForm
from .tables import FlightTable
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django_tables2 import RequestConfig
import django_tables2


class FilteredSingleTableView(django_tables2.SingleTableView):
    filter_class = None

    def get_table_data(self):
        self.filter = self.filter_class(self.request.GET, queryset=super(FilteredSingleTableView, self).get_table_data() )
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


def passengers_list(request):
        passengers = Passenger.objects.all().order_by('surname')
        return render(request, 'flights/passengers_list.html', {'passengers': passengers})


def flights_list(request):
    table = FlightTable(Flight.objects.all())
    table.objects.annotate(date_only=Cast('date', DateField()))
    RequestConfig(request).configure(table)
    return render(request, 'flights/flights_list.html', {'table': FilteredSingleTableView})


def flights_detail(request, pk):
    flight = Flight.objects.get(pk=pk)
    error = False
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            if flight.airplane.capacity >= flight.ticketsPurchased + passenger.nrOfTickets:
                passenger.save()
                flight.passengers.add(passenger)
                flight.add_tickets(passenger.nrOfTickets)
            else:
                error = True
    else:
        form = PassengerForm()
    return render(request, 'flights/flights_detail.html', {'flight': flight, 'pk': pk, 'form': form, 'error': error})


def flights_auth(request):
    context = {}
    return render(request, 'flights/templates/flights/registration/login.html', context)

