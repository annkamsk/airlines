from .models import Flight
import django_filters


class FlightFilter(django_filters.FilterSet):

    class Meta:
        model = Flight
        exclude = ('airplane', 'ticketsPurchased', 'passengers')

