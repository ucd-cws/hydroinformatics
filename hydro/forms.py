__author__ = 'nicksantos'

import models
from django.forms import ModelForm

class StationForm(ModelForm):
	class Meta:
		model = models.Station

class RiverForm(ModelForm):
	class Meta:
		model = models.River