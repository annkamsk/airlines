from django.contrib import admin
from .models import Flight, Passenger, Airplane, Airport, Crew

admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Crew)