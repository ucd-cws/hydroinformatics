__author__ = 'nrsantos'

import datetime
import time

from celery import task
from hydro.models import Image

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

	site = image.site  # TODO: Needs to pull the site out of the image, if possible

	image.timestamp_raw = common.image.extract_value_from_exif(
		image.image.path,
		image.camera.time_exif_field,
		image.camera.time_regex,
		1
	)

	ldt = datetime.datetime.strptime(image.timestamp_raw, "%m/%d/%y %I:%M %p")  # " month/day/year hour:minute AM/PM
	image.timestamp_seconds = time.mktime(ldt.timetuple())
	image.timestamp = ldt  # image.timestamp is a datetime field, so we should be able to just assign directly

	# TODO: Needs to check if it has baro first
	if image.camera.has_baro:
		image.baro_value = common.image.extract_value_from_exif(
			image.image.path,
			image.camera.baro_exif_field,
			image.camera.baro_regex,
			1
		)

	image.sun_angle = Pysolar.GetAltitude(site.lat, site.lon, ldt.utctime())

	image.is_processed = True
	image.save()