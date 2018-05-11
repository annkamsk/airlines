import random
from flights.models import *
from datetime import datetime, timedelta


fileAirports = open('airlines/data/airports_data.txt', "r")
for f in fileAirports:
    f = f.strip()
    a = Airport(name=f)
    a.save()

random.seed(None)

fileAirplanes = open('airlines/data/airplanes.txt', "r")
for f in fileAirplanes:
    f = f.strip()
    a = Airplane(licenseChars=f, capacity=random.randint(20, 500))
    a.save()


airports = Airport.objects.all()
airplanes = Airplane.objects.all()
date = datetime.now()
for airplane in airplanes:
    for i in range(50):
        flight = Flight(airplane=airplane, startingAirport=airports[i],
                        landingAirport=airports[(i + 1) % airports.__sizeof__()],
                        startingTime=date, landingTime=date + timedelta(days=0, hours=random.randint(1, 14),
                                                                        minutes=random.randint(0, 59)))
        date += timedelta(days=1, hours=8)
        flight.save()
