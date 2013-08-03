__author__ = 'nrsantos'

import datetime
import time
import pytz

from celery.task import task
from hydro.models import Image, Site

try:
	import Pysolar
except ImportError:
	import Pysolar_backup as Pysolar  # keeping a local copy in the repo. Prefer to use system copy, but this way if the dependency disappears, we still have it

try:
	from code_library import common
except ImportError:
	from code_library_backup import common  # same deal, except this copy is pared down to remove the arcpy dependency and only include the image tools


@task()
def process_image(image_id):
	image = Image.objects.get(pk=image_id)
	if image.is_processed is True:  # we don't need to do it again
		return

	if not image.site and image.camera.has_site:  # if we haven't already set the site and we can get it instead from the camera
		t_site = common.image.extract_value_from_exif( # grab the site information from the camera
			image.image.path,
			image.camera.site_exif_field,
			image.camera.site_regex,
			1,
		)
		try:
			image.site = Site.objects.get(shortcode=t_site)
		except Site.DoesNotExist:
			print "Could not assign site to image %s - site name = %s" % (image.pk, t_site)

	image.timestamp_raw = common.image.extract_value_from_exif(
		image.image.path,
		image.camera.time_exif_field,
		image.camera.time_regex,
		1  # 1 is the capture group number
	)

	# TODO: Add timezone support. More confusing than I can handle right now
	ldt = datetime.datetime.strptime(image.timestamp_raw, "%m/%d/%y %I:%M %p")  # " month/day/year hour:minute AM/PM
	image.timestamp_seconds = time.mktime(ldt.timetuple())
	image.timestamp = ldt  # image.timestamp is a datetime field, so we should be able to just assign directly
	t = time.gmtime(image.timestamp_seconds)
	image.timestamp_utc = utc_datetime = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, tzinfo=pytz.utc)


	if image.camera.has_baro:
		image.baro_value = common.image.extract_value_from_exif(
			image.image.path,
			image.camera.baro_exif_field,
			image.camera.baro_regex,
			1  # 1 is the capture group number
		)

	if image.site and image.site.lat and image.site.lon:
		# if we have a site, then we can get the sun angle

		image.sun_angle = Pysolar.GetAltitude(image.site.lat, image.site.lon, utc_datetime)
		image.daytime_check()

	image.is_processed = True
	image.save()