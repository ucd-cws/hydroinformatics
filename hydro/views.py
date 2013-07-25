# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext
from django.template.loader import render_to_string
from django.core import exceptions

import logging

from Hydroinformatics import settings
import models
import forms
#import utils

import simplejson

# Get an instance of a logger
log = logging.getLogger(__name__)


def home(request):
	template = loader.get_template("index.django")
	cont = RequestContext(request, {})
	return HttpResponse(template.render(cont))


def data_sources(request):
	stations = models.Station.objects.all()

	template = loader.get_template("listing.django")
	cont = RequestContext(request, {'objects': stations, 'section_title': "Data Sources (USGS Stations)", })

	return HttpResponse(template.render(cont))


def add_data_source(request):
	if request.method == "GET":

		data_source_form = forms.StationForm()

		template = loader.get_template("form.django")
		cont = RequestContext(request,
								{'form': data_source_form, 'section_title': "Data Sources", 'subtitle': 'Add Station'})
		return HttpResponse(template.render(cont))
	elif request.method == "POST":
		data_source_form = forms.StationForm(request.POST)
		template = loader.get_template("subpage.django")

		if data_source_form.is_valid():
			data_source_form.save()
			cont = RequestContext(request, {'content_html': 'Station created', 'section_title': "Data Sources", })
		else:
			cont = RequestContext(request, {'content_html': 'Error creating station', 'section_title': "Data Sources", })

		return HttpResponse(template.render(cont))


def single_data_source(request, source_id):
	station = models.Station.objects.get(pk=source_id)

	template = loader.get_template("station.django")
	cont = RequestContext(request, {'section_title': "Data Sources", 'subtitle': station.name, 'station': station})
	return HttpResponse(template.render(cont))


def add_river(request):
	if request.method == "GET":

		river_form = forms.RiverForm()

		template = loader.get_template("form.django")
		cont = RequestContext(request, {'form': river_form, 'section_title': "Rivers", })
		return HttpResponse(template.render(cont))
	elif request.method == "POST":
		river_form = forms.RiverForm(request.POST)
		template = loader.get_template("subpage.django")

		if river_form.is_valid():
			river_form.save()
			cont = RequestContext(request, {'content_html': 'River created', 'section_title': "Rivers", })
		else:
			cont = RequestContext(request, {'content_html': 'Error creating river', 'section_title': "Rivers", })

		return HttpResponse(template.render(cont))


def rivers(request):
	rivers = models.River.objects.all().order_by('name')

	template = loader.get_template("listing.django")
	cont = RequestContext(request, {'objects': rivers, 'section_title': "Rivers", })

	return HttpResponse(template.render(cont))


def single_river(request, river_id=None):
	river = get_object_or_404(models.River, pk=river_id)
	sources_stations = models.Station.objects.filter(river=river.pk)
	sources_sites = models.Site.objects.filter(river=river.pk)

	template = loader.get_template("river.django")
	cont = RequestContext(request,
						  {'river': river, 'sources_stations': sources_stations, 'sources_sites': sources_sites,
						   'section_title': "Rivers", })

	return HttpResponse(template.render(cont))


def sites(request):
	sites = models.Site.objects.all()

	template = loader.get_template("listing.django")
	cont = RequestContext(request, {'objects': sites, 'section_title': "Sites", })

	return HttpResponse(template.render(cont))