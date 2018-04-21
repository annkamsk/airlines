import django_filters as df
from .models import Flight

class FlightFilter(df.FilterSet):
    class Meta:
        fields = Flight