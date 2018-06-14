from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Airplane(models.Model):
    licenseChars = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.licenseChars


class Airport(models.Model):
    name = models.CharField(max_length=100, default='Airport')

    def __str__(self):
        return self.name


class Passenger(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    nrOfTickets = models.IntegerField(default=0, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name + ' ' + self.surname


class Crew(models.Model):
    captain_name = models.CharField(max_length=30)
    captain_surname = models.CharField(max_length=40)

    def __str__(self):
        return self.captain_name + ' ' + self.captain_surname


class Flight(models.Model):
    startingAirport = models.ForeignKey(Airport, related_name='%(class)s_startingAirport', on_delete=models.CASCADE)
    startingTime = models.DateTimeField(default=timezone.now)
    landingAirport = models.ForeignKey(Airport, related_name='%(class)s_landingAirport', on_delete=models.CASCADE)
    landingTime = models.DateTimeField(default=timezone.now)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    ticketsPurchased = models.IntegerField(default=0)
    crew = models.ForeignKey(Crew, related_name='%(class)s_crew', on_delete=models.CASCADE)

    def add_tickets(self, nr):
        self.ticketsPurchased += nr

    @property
    def passengerslist(self):
        return list(self.passengers.all())

    def starting_date_parser(self):
        return self.startingTime.date()

    def starting_time_parser(self):
        return self.startingTime.time().strftime('%H:%M')

    def landing_time_parser(self):
        return self.landingTime.time().strftime('%H:%M')

    def clean(self):
        flights = Flight.objects.filter(crew=self.crew)
        for f in flights:
            if f.id != self.id and not(f.startingTime > self.landingTime or f.landingTime < self.startingTime):
                raise ValidationError("busy")

    def __str__(self):
        return self.startingAirport.name + '-' + self.landingAirport.name + ': ' + self.startingTime.__str__()









