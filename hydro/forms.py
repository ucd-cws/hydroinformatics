__author__ = 'nicksantos'

import models
from django import forms
from django.forms import Form,ModelForm

class StationForm(ModelForm):
	class Meta:
		model = models.Station

class RiverForm(ModelForm):
	class Meta:
		model = models.River

class StationDateForm(Form):
	date_start = forms.DateField()
	date_end = forms.DateField()
	#station =

class ImageUploadForm(Form): # or should this be a model form?
	pass