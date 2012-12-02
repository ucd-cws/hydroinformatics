# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext
from django.template.loader import render_to_string
from django.core import exceptions

from Hydroinformatics import settings
import models
import forms
#import utils

import simplejson

def log(msg):
	# 	TODO: needs to be fized by the time we go live

	print msg


def home(request):

	template = loader.get_template("index.django")
	cont = RequestContext(request,{})
	return HttpResponse(template.render(cont))


def data_sources(request):
	stations = models.Station.objects.all()

	template = loader.get_template("listing.django")
	cont = RequestContext(request,{'objects':stations, 'section_title':"Data Sources (USGS Stations)",})

	return HttpResponse(template.render(cont))


def add_data_source(request):

	if request.method == "GET":

		data_source_form = forms.StationForm()

		template = loader.get_template("form.django")
		cont = RequestContext(request,{'form':data_source_form,'section_title':"Data Sources",'subtitle':'Add Station'})
		return HttpResponse(template.render(cont))
	elif request.method == "POST":
		data_source_form = forms.StationForm(request.POST)
		template = loader.get_template("subpage.django")

		if data_source_form.is_valid():
			data_source_form.save()
			cont = RequestContext(request,{'content_html':'Station created', 'section_title':"Data Sources",})
		else:
			cont = RequestContext(request,{'content_html':'Error creating station', 'section_title':"Data Sources",})

		return HttpResponse(template.render(cont))

def add_river(request):
	if request.method == "GET":

		river_form = forms.RiverForm()

		template = loader.get_template("form.django")
		cont = RequestContext(request,{'form':river_form, 'section_title':"Rivers",})
		return HttpResponse(template.render(cont))
	elif request.method == "POST":
		river_form = forms.RiverForm(request.POST)
		template = loader.get_template("subpage.django")

		if river_form.is_valid():
			river_form.save()
			cont = RequestContext(request,{'content_html':'River created', 'section_title':"Rivers",})
		else:
			cont = RequestContext(request,{'content_html':'Error creating river', 'section_title':"Rivers",})

		return HttpResponse(template.render(cont))

def rivers(request):
	rivers = models.River.objects.all()

	template = loader.get_template("listing.django")
	cont = RequestContext(request,{'objects':rivers, 'section_title':"Rivers",})

	return HttpResponse(template.render(cont))
