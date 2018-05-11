from django import forms
from django.forms import DateInput

from .models import Passenger, Flight
from datetime import datetime


class PassengerForm(forms.ModelForm):

    class Meta:
        model = Passenger
        fields = ('name', 'surname', 'nrOfTickets')


class FlightForm(forms.ModelForm):
    fromDateStart = forms.DateTimeField(label='start from date: YYYY-MM-DD',
                                         required=False)
    toDateStart = forms.DateTimeField(label='start to date: YYYY-MM-DD',required=False)
    fromDateLand = forms.DateTimeField(label='landing from date: YYYY-MM-DD',
                                        required=False)
    toDateLand = forms.DateTimeField(label='landing to date: YYYY-MM-DD',
                                      required=False)

    class Meta:
        model = Flight
        fields = ('startingAirport', 'landingAirport')
        widgets = {

        }

