from django.shortcuts import render
from .models import Passenger, Flight
from .forms import PassengerForm, FlightForm
from .tables import FlightTable
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
    allf = Flight.objects.all()
    if request.method == "GET":
        form = FlightForm(request.GET)
        if form.is_valid():
            flight = form.save(commit=False)
            fds=request.GET.get('fromDateStart', default='')
            fdl=request.GET.get('fromDateLand', default='')
            tds=request.GET.get('toDateStart', default='')
            tdl=request.GET.get('toDateLand', default='')

            if fds != '':
                allf = allf.filter(startingTime__gte=fds)
            if fdl != '':
                allf = allf.filter(landingTime__gte=fdl)
            if tds != '':
                allf = allf.filter(startingTime__lte=tds)
            if tdl != '':
                allf = allf.filter(landingTime__lte=tdl)
            table = FlightTable(allf.filter(landingAirport=flight.landingAirport, startingAirport=flight.startingAirport))
    else:
        form = FlightForm()

    RequestConfig(request, paginate={"per_page": 20}).configure(table)
    return render(request, 'flights/flights_list.html', {'table': table, 'form': form})


def flights_detail(request, pk):
    flight = Flight.objects.select_for_update().get(pk=pk)
    error = False
    errorname = False
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            if not(passenger.name.isalpha() and passenger.surname.isalpha()):
                errorname = True

            elif flight.airplane.capacity >= flight.ticketsPurchased + passenger.nrOfTickets:
                passenger.save()
                flight.passengers.add(passenger)
                flight.add_tickets(passenger.nrOfTickets)
                flight.save()
            else:
                error = True
    else:
        form = PassengerForm()
    tickets = flight.airplane.capacity - flight.ticketsPurchased
    return render(request, 'flights/flights_detail.html', {'flight': flight, 'pk': pk, 'form': form, 'error': error,
                                                           'tickets': tickets, 'errorname': errorname})


def flights_auth(request):
    context = {}
    return render(request, 'flights/templates/flights/registration/login.html', context)

