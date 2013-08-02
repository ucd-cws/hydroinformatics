__author__ = 'nrsantos'

from django.core.files.uploadedfile import UploadedFile
import tasks

try:
	import Pysolar
except ImportError:
	import Pysolar_backup as Pysolar  # keeping a local copy in the repo. Prefer to use system copy, but this way if the dependency disappears, we still have it

try:
	from code_library import common
except ImportError:
	from code_library_backup import common  # same deal, except this copy is pared down to remove the arcpy dependency and only include the image tools

from celery.task import Task

def make_temp_photo(path):
	return UploadedFile(open(path, 'rb'))

def add_image(file_path, site_code, move_to = False):
	"""
		Adds an image to a site

	:param file_path:
	:param site_code:
	:param move_to:
	"""

def process_image_list(images):
	"""
		given a list (or queryset) of image objects, initializes processing, then returns
	"""

	for image in images:  # using id instead of object because it's asynchronous and could be fetched off of any system at any time - even  after changes are made
		tasks.process_image(image.id).delay()

