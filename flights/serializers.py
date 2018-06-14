from rest_framework import serializers

from flights.models import Crew, Flight


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    From = serializers.CharField(source='startingAirport.name')
    To = serializers.CharField(source='landingAirport.name')
    crew = serializers.CharField(source='crew.captain_surname')
    date = serializers.DateField(source='starting_date_parser')
    start = serializers.TimeField(source='starting_time_parser')
    landing = serializers.TimeField(source='landing_time_parser')

    class Meta:
        model = Flight
        fields = ('id', 'From', 'To', 'date', 'start', 'landing', 'crew')
