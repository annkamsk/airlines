from django.shortcuts import render
from .models import Passenger, Flight, Airport
from .forms import PassengerForm, FlightForm
from .tables import FlightTable
from django_tables2 import RequestConfig


def passengers_list(request):
        passengers = Passenger.objects.all().order_by('surname')
        return render(request, 'flights/passengers_list.html', {'passengers': passengers})


def flights_list(request):
    flights = Flight.objects.all().order_by('startingTime')[:100]
    airports = Airport.objects.all()
    if request.method == "GET":
        fds = request.GET.get('fromDateStart', default='')
        tds = request.GET.get('toDateStart', default='')
        sa = request.GET.get('startingAirport', default='')
        la = request.GET.get('landingAirport', default='')

        if sa != '' or la != '' or fds != '' or tds != '':
            flights = Flight.objects.all()

            if sa != '':
                flights = flights.filter(startingAirport=sa)
            if la != '':
                flights = flights.filter(landingAirport=la)
            if fds != '':
                flights = flights.filter(startingTime__gte=fds)
            if tds != '':
                flights = flights.filter(startingTime__lte=tds)

    return render(request, 'flights/flights_list.html', {'table': flights, 'airports': airports})


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

