from django import forms
from .models import Passenger, Flight, Airport, Crew


class PassengerForm(forms.ModelForm):

    class Meta:
        model = Passenger
        fields = ('name', 'surname', 'nrOfTickets')


class FlightForm(forms.ModelForm):
    startingAirport = forms.ModelChoiceField(label='starting airport', required=False,
                                             queryset=Airport.objects.all(), empty_label=None
                                             )
    landingAirport = forms.ModelChoiceField(label='landing airport', required=False,
                                            queryset=Airport.objects.all())
    fromDateStart = forms.DateTimeField(label='start from date:', required=False,
                                        widget=forms.widgets.SelectDateWidget)
    toDateStart = forms.DateTimeField(label='start to date:', required=False,
                                      widget=forms.widgets.SelectDateWidget)

    class Meta:
        model = Flight
        fields = ()


class CrewForm(forms.ModelForm):
    flight = forms.ModelChoiceField(queryset=Flight.objects.all())
    captain = forms.ModelChoiceField(queryset=Crew.objects.all())

    class Meta:
        model = Crew
        fields = ()


