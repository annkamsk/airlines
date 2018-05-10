import time
import random
from flights.models import *
from datetime import datetime, timedelta
from random import randint


# READING FILES
# ADDING airports
fileAirports = open('airlines/data/airports_data.txt', "r")
for x in fileAirports:
    x = x.strip()
    t = Airport(name=x)
    t.save()

random.seed(None)

filePlanes = open('airlines/data/airplanes.txt', "r")
for x in filePlanes:
    x = x.strip()
    t = Airplane(licenseChars=x, capacity=random.randint(20, 500))
    t.save()

# # ADDING flights
airports = Airport.objects.all()
airplanes = Airplane.objects.all()
date = datetime.now()
for airplane in airplanes:
    for i in range(50):
        flight = Flight(airplane=airplane, startingAirport=airports[i],
                        landingAirport=airports[(i + 1) % airports.__sizeof__()],
                        startingTime=date, landingTime=date + timedelta(days=0, hours=random.randint(2, 14),
                                                                        minutes=random.randint(0, 59)))
        date += timedelta(days=1, hours=6, minutes=15)
        flight.save()
