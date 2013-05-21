from django.db import models

# Create your models here.

class River(models.Model):
	name = models.CharField(max_length = 255)

	def __unicode__(self):
		return self.name


class Station(models.Model):
	name = models.CharField(max_length = 255)
	source_url = models.URLField(default="http://waterservices.usgs.gov/nwis/iv/?")
	usgs_id = models.IntegerField()
	river = models.ForeignKey(River)
	lat = models.FloatField(null=True,)
	lon = models.FloatField(null=True,)

	def __unicode__(self):
		return self.name

	def retrieve_station_data(self):
		pass

class Graph(models.Model):
	pass

class Site(models.Model):
	name = models.CharField(max_length=255)
	river = models.ForeignKey(River)
	lat = models.FloatField(null=True,)
	lon = models.FloatField(null=True,)
	notes = models.TextField()

class User(models.Model):
	name = models.CharField(max_length=30)

class Video(models.Model):
	user = models.ForeignKey(User)
	sites = models.ManyToManyField(Site)
	stations = models.ManyToManyField(Station)
	width = models.IntegerField()
	height = models.IntegerField()
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()

class Image(models.Model):
	location = models.CharField(max_length=255) # where it is on the filesystem
	width = models.IntegerField()
	height = models.IntegerField()

class ImageGraphPair(models.Model):
	"""
		This class acts as the individual river frame. We may want the ability
		to
	"""
	video = models.ForeignKey(Video)
	image = models.ForeignKey(Image)
	graph = models.ForeignKey(Graph)

class Frame(models.Model):
	video = models.ForeignKey(Video)
	duration = models.IntegerField(default=100) # in milliseconds
	timestamp = models.DateTimeField()
	time_from = models.DateTimeField() # the beginning moment of the time this covers (as the camera perceives it, not the video)
	time_to = models.DateTimeField() # the end moment of the time period this covers

class SingleFrame(Frame):
	"""
		A single frame has all the attributes above, plus an image graph pair
	"""
	image = models.ForeignKey(ImageGraphPair, related_name='main_image')

class MultiFrame(Frame):
	"""
		MultiFrame would be used pair many frames together.
		Many to Many relationship lets us expand this in the future
	"""
	images = models.ManyToManyField(ImageGraphPair)

class Plugin(models.Model):
	"""
		A base class
	"""

	def register(self):
		pass

class GraphPlugin(Plugin):
	"""
		Has all the plugin methods, plus some particular to graphing.
		A future plugin for this could be one specific to calling an external script
		to make the graphs (like R). It would have a path to the script and arguments
		including the path to a data csv and an output location, then it would write
		out the time series data to that csv, expect the images in the output location,
		along with some sort of manifest file that it could read back in and add to the
		database.
	"""

class DataType(models.Model):
	name = models.CharField(max_length=255)

class DataSeries(models.Model):
	station = models.ForeignKey(Station)
	datatype = models.ForeignKey(DataType)

class DataPoint(models.Model):
	dataseries = models.ForeignKey(DataSeries)
	datatype = models.ForeignKey(DataType)

class GraphSeries(models.Model):
	"""
		maps DataSeries to graphs. Not using built in ManyToMany because we want to add some attributes in the mapping
		Still just a definition. Actual graphs are made as GraphInstances
	"""
	graph = models.ForeignKey(Graph)
	series = models.ForeignKey(DataSeries)
	color = models.CharField(max_length = 10) # in hex
	line_width = models.SmallIntegerField()

class GraphInstance(models.Model):
	location = models.CharField(max_length=255) # where it is on the filesystem
	graph_type = models.ForeignKey(Graph)
	timestamp = models.DateTimeField()
	time_from = models.DateTimeField() # the beginning moment of the time this covers
	time_to = models.DateTimeField() # the end moment of the time period this covers