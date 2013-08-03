from django.db import models


class River(models.Model):
	name = models.CharField(max_length = 255)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return unicode(self.name)


class Station(models.Model):
	name = models.CharField(max_length=255)
	source_url = models.URLField(default="http://waterservices.usgs.gov/nwis/iv/?")
	usgs_id = models.IntegerField()
	river = models.ForeignKey(River)
	lat = models.FloatField(null=True,)
	lon = models.FloatField(null=True,)

	def __unicode__(self):
		return unicode(self.name)

	def __str__(self):
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
	representative_photo = models.ImageField(upload_to="photos/sites/%Y/%m")
	shortcode = models.CharField(max_length=10, unique=True)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return unicode(self.name)


class User(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return unicode(self.name)


class Camera(models.Model):
	name = models.CharField(max_length=100)
	model_name = models.CharField(max_length=100, null=True)

	time_exif_field = models.CharField(max_length=50)  # the metadata field we'll grab the time from
	time_regex = models.CharField(max_length=255)  # regex to extract the time data

	has_baro = models.BooleanField(default=False)
	baro_exif_field = models.CharField(max_length=50, null=True)  # the metadata field we'll grab the time from
	baro_regex = models.CharField(max_length=255, null=True)  # regex to extract the time data
	baro_units = models.CharField(max_length=10, null=True)

	has_site = models.BooleanField(default=False)
	site_exif_field = models.CharField(max_length=50, null=True)  # the metadata field we'll grab the site from
	site_regex = models.CharField(max_length=255, null=True)  # regex to extract the time data

	representative_photo = models.ImageField(upload_to="photos/cameras/%Y/", null=True)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return unicode(self.name)

class Image(models.Model):
	image = models.ImageField(upload_to='self.get_location', width_field="width", height_field="height")  # where it is on the filesystem
	width = models.IntegerField()
	height = models.IntegerField()
	site = models.ForeignKey(Site, null=True) # these should all be defined, but it's possible that it'll be added in processing
	sun_angle = models.DecimalField(max_digits=12, decimal_places=10, null=True)

	baro_value = models.DecimalField(max_digits=12, decimal_places=10, null=True)
	timestamp = models.DateTimeField(null=True)
	timestamp_raw = models.CharField(max_length=25, null=True)
	timestamp_seconds = models.IntegerField(null=True)  # so we can easily compare to other images and items
	timestamp_utc = models.DateTimeField(null=True)
	camera = models.ForeignKey(Camera)

	daytime_buffer = models.SmallIntegerField(max_length=3, default=5)

	is_processed = models.BooleanField(default=False)  # flag we set to indicate whether or not the image is ready to use
	is_daytime = models.BooleanField(default=False)

	def get_location(self):
		return "photos/sites/" + self.site + "/%Y/%m/%d"

	def daytime_check(self):
		if self.sun_angle > (0-self.daytime_buffer):
			self.is_daytime = True
			return True
		else:
			self.is_daytime = False
			return False

	def is_nighttime(self):
		return not self.is_daytime()

class Video(models.Model):
	user = models.ForeignKey(User)
	sites = models.ManyToManyField(Site)
	stations = models.ManyToManyField(Station)
	width = models.IntegerField()
	height = models.IntegerField()
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()
	images = models.ManyToManyField(Image)
	graphs = () ## TODO: Add field for storing multiple graph plugin keys
	formatter = () # TODO: Add formatter object. Specifies the layout of the video. Should have a represenation and accept a list of images and a list of graphs and return a frame



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