__author__ = 'nrsantos'

import datetime
import time
import pytz
import arrow  # times for non-crazy people

import ulmo

import Image as PIL # need to rename it or it collides with our model

from hydro.models import Image, Site
from Hydroinformatics.settings import image_sizes

from celery import task

try:
	import Pysolar
except ImportError:
	import Pysolar_backup as Pysolar  # keeping a local copy in the repo. Prefer to use system copy, but this way if the dependency disappears, we still have it

try:
	from code_library import common
except ImportError:
	from code_library_backup import common  # same deal, except this copy is pared down to remove the arcpy dependency and only include the image tools


@task()
def process_image(image_id, exif_registry=None):
	image = Image.objects.get(pk=image_id)
	if image.is_processed is True:  # we don't need to do it again
		return

	if not image.site and image.camera.has_site:  # if we haven't already set the site and we can get it instead from the camera
		t_site = common.image.extract_value_from_exif( # grab the site information from the camera
			image.image.path,
			image.camera.site_exif_field,
			image.camera.site_regex,
			1,
			exif_registry=exif_registry
		)
		try:
			image.site = Site.objects.get(shortcode=t_site)
		except Site.DoesNotExist:
			print "Could not assign site to image %s - site name = %s" % (image.pk, t_site)

	image.timestamp_raw = common.image.extract_value_from_exif(
		image.image.path,
		image.camera.time_exif_field,
		image.camera.time_regex,
		1,  # 1 is the capture group number
		exif_registry=exif_registry
	)

	ldt = arrow.get(image.timestamp_raw, "%m/%d/%y %I:%M %p", 'US/Pacific')  # " month/day/year hour:minute AM/PM
	# TODO: For now, hardcoding in US/Pacific. In the future, this should be per site
	image.timestamp_seconds = ldt.timestamp
	image.timestamp = ldt.datetime  # image.timestamp is a datetime field, so we should be able to just assign directly
	image.timestamp_utc = utc_datetime = ldt.to('utc').timestamp

	if image.camera.has_baro:
		image.baro_value = common.image.extract_value_from_exif(
			image.image.path,
			image.camera.baro_exif_field,
			image.camera.baro_regex,
			1,  # 1 is the capture group number
			exif_registry=exif_registry
		)

	if image.site and image.site.lat and image.site.lon:
		# if we have a site, then we can get the sun angle

		image.sun_angle = Pysolar.GetAltitude(image.site.lat, image.site.lon, utc_datetime)
		image.daytime_check()

	image.save()  # save once - we need it to populate the width/height fields and move the file to proper location

	# generate thumbnails now
	# TODO: make a make thumbnails method that can process additional sizes
	"""for size in image_sizes:
		if size > image.width:  # if it's a larger size, skip it
			continue

		t_size = size, size

		thumb = PIL.open(image.image.path)
		thumb.thumbnail(t_size, PIL.ANTIALIAS)
	#	thumb.save()
	"""

	image.is_processed = True
	image.save()