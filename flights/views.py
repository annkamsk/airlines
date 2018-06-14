from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics, renderers, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from flights.serializers import CrewSerializer, FlightSerializer
from .models import Passenger, Flight, Airport, Crew
from .forms import PassengerForm


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


@transaction.atomic
def flights_detail(request, pk):
    flight = Flight.objects.select_for_update().get(pk=pk)
    error = False
    errorname = False
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            if not (passenger.name.isalpha() and passenger.surname.isalpha()):
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


@csrf_exempt
def user_authenticate(request):
    if request.method == "POST":
        if authenticate(username=request.POST['user'], password=request.POST['password']) is not None:
            return JsonResponse({'loggedin': 'true'}, safe=False)
    return JsonResponse({'loggedin': 'false'}, safe=False)


@transaction.atomic
def assign_crew(request):
    if request.method == 'POST':
        flight_id = request.POST.get('flight', None)
        crew_id = request.POST.get('crew', None)
        flight = Flight.objects.all().get(pk=flight_id)
        crew = Crew.objects.all().get(pk=crew_id)
        flight.crew = crew
        flight.save()
        try:
            flight.full_clean()
        except ValidationError as e:
            return JsonResponse({'result': 'busy'})

        return JsonResponse({'result': 'successful'})

    return JsonResponse({'result': 'error'})


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'crews': reverse('crew-list', request=request, format=format)
    })


class FlightList(generics.ListAPIView):
    queryset = Flight.objects.all().order_by('startingTime')[:100]
    serializer_class = FlightSerializer
    renderer_classes = (renderers.JSONRenderer,)


class CrewList(generics.ListAPIView):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    renderer_classes = (renderers.JSONRenderer,)
