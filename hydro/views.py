# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext



#for graphing
from pylab import *
from mlgraph import test
import logging

#for grabbing files from the storage system
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import Storage
from django.core.files.base import ContentFile


#from hydro.plugins.formatters import IFormatterRegistry
import models
import forms
#import utils

# Get an instance of a logger
log = logging.getLogger(__name__)

#matplotlib PNG image and storage
def graph(reguest):
	#CSV files stored statically, local backend
	#fileName should be in request or another parameter? Have to look up as well
	fileStorage = FileSystemStorage(location=BASE_DIR) #BASE_DIR = "path to media"???
	if fileStorage.exsists(fileName):
		print ("it exsists") #log it not print it have to look that up
	else:
		print ("it doesn't") #actually log it instead and send out error and render an error http webpage

	file = fileStorage.open(fileName, mode='r') # to read it

	#construct the graph

    #read and format csv data
	#store the image as a string buffer
	#send buffer in a httpresponse with the mime type image/png set




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
	graphs = models.Graphs.objects.all()
	
	template = loader.get_template("listing.django")
	cont = RequestContext(request, {'objects': graphs, 'section_title': "Graphs", })
		
	return HttpResponse(template.render(cont))