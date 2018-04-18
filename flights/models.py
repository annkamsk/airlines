from django.db import models
from django.utils import timezone


class Airplane(models.Model):
    licenseChars = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.licenseChars



class Airport(models.Model):
    name = models.CharField

    def __str__(self):
        return self.name



class Passenger(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)

    def __str__(self):
        return self.name + ' ' + self.surname


class Flight(models.Model):
    startingAirport = models.ForeignKey(Airport, related_name='%(class)s_startingAirport', on_delete=models.CASCADE)
    startingTime = models.DateTimeField(default=timezone.now)
    landingAirport = models.ForeignKey(Airport, related_name='%(class)s_landingAirport', on_delete=models.CASCADE)
    landingTime = models.DateTimeField(default=timezone.now)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)


    @property
    def passengerslist(self):
        return list(self.passengers.all())

    def __str__(self):
        return self.startingAirport + '-' + self.landingAirport + ': ' + self.startingTime







