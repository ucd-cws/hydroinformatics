# Create your views here.
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image, StringIO
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter
from collections import defaultdict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext
from django.template.loader import render_to_string
from django.core import exceptions
from django.views import generic
from django.views.decorators.csrf import csrf_exempt


import logging

from Hydroinformatics import settings
#from hydro.plugins.formatters import IFormatterRegistry
import models
import forms
#import utils

import simplejson

# Get an instance of a logger
log = logging.getLogger(__name__)


class site_detail_view(generic.DetailView):
	model = models.Site
	context_object_name = "detail_object"

	def get_context_data(self, *args, **kwargs):
		# Call the base implementation first to get a context
		context = super(generic.DetailView, self).get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['section_title'] = "Sites"
		context['photo'] = context['detail_object'].representative_photo.url
		return context


class list_processed_photos(generic.ListView):
	queryset = models.Image.objects.filter(is_processed=True).order_by('sun_angle')
	context_object_name = "images"
	template_name = "images.django"


def home(request):
	template = loader.get_template("index.django")
	cont = RequestContext(request, {})
	return HttpResponse(template.render(cont))


def process(request, plugin,):
	if plugin in IFormatterRegistry.plugins_by_name:
		formatter = IFormatterRegistry.plugins_by_name[plugin]
		entry_point = formatter._get_process_entry_hook()
		if entry_point is not None:
			entry_point()


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

def add_graph(request):
	errors = []
	if request.method == "POST":
		graph_form = forms.GraphForm(request.POST, request.FILES)
		template = loader.get_template("subpage.django")
		if graph_form.is_valid():
			graph_form.save()
			cont = RequestContext(request, {'content_html': 'Graph created', 'section_title': "Graphs", })
		else:
			errors.append(graph_form.errors)
			cont = RequestContext(request, {'content_html': 'Error creating graph', 'section_title': "Graphs",'Errors':errors })
	else:
		graph_form = forms.GraphForm()
		template = loader.get_template("form.django")
		cont = RequestContext(request, {'form': graph_form, 'section_title': "Graph", })

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


def graphs(request):
	graphs = models.Graph.objects.all()

	template = loader.get_template("listing.django")
	cont = RequestContext(request, {'objects': graphs, 'section_title': "Graphs", })

	return HttpResponse(template.render(cont))


def single_graph(request, graph_id=None):
	graph = get_object_or_404(models.Graph, pk=graph_id)

	template = loader.get_template("graph.django")
	cont = RequestContext(request, {'graph': graph, 'section_title': "Graph", })

	return HttpResponse(template.render(cont))





def render_graph(request, graph_id=None):
	graph = get_object_or_404(models.Graph, pk=graph_id)
	data = np.genfromtxt(graph.data, delimiter=',', names=['x','y']) #extract data from cvs after x and y

	fig = plt.Figure()
	#ax = fig.add_subplot(111)

	#ani = animation.FuncAnimation(fig, update, 25, fargs=(data),
  #  interval=50, blit=True)
  	fig.plot(data['x'], data['y'], label=graph.name)
	canvas=FigureCanvas(fig)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return(response)

#deletes graph and returns to listings
@csrf_exempt
def delete_graph(request, graph_id=None):
	if request.is_ajax():
		try:
			deleted = models.Graph.objects.get(pk=request.POST.get('id'));
			deleted.delete()
			#return to listings
			graphs = models.Graph.objects.all()
			template = loader.get_template("listing.django")
			cont = RequestContext(request, {'objects': graphs, 'section_title': "Graphs", })
		except:
			template = loader.get_template("graph.django")
			cont = RequestContext(request, {'content_html': 'Error deleting graph', 'section_title': "Graphs" })

	else:
		template = loader.get_template("graph.django")
		cont = RequestContext(request, {'content_html': 'Error deleting graph', 'section_title': "Graphs" })
	return HttpResponse(template.render(cont))

def update(data):
		xarr = []
		yarr =[]
		for line in data:
			x = line[0]
			y = line[1]
			xarr.append(int(x))
			yarr.append(int(y))
