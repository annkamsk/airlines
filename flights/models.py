from django.db import models
from django.utils import timezone


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
        return self.startingAirport.name + '-' + self.landingAirport.name + ': ' + self.startingTime.__str__()


class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Customer(models.Model):
    company = models.ForeignKey('Company', null=False, on_delete='models.CASCADE')
    customer_first_name = models.CharField(null=False, blank=False, max_length=50)
    customer_last_name = models.CharField(null=False, blank=False, max_length=50)
    customer_email = models.CharField(null=False, blank=False, max_length=80)
    account_number = models.CharField(null=False, blank=False, max_length=20)
    address1 = models.CharField(null=False, blank=False, max_length=50)
    address2 = models.CharField(null=False, blank=False, max_length=20)
    city = models.CharField(null=False, blank=False, max_length=50)
    state = models.CharField(null=False, blank=False, max_length=2)
    customer_email = models.CharField(null=False, blank=False, max_length=80)
    primary_phone = models.CharField(null=False, blank=False, max_length=12)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


ordering = ['-id']





