from django.contrib import admin
from .models import Flight, Passenger, Airplane, Airport

admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Airplane)
admin.site.register(Airport)