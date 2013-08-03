__author__ = 'Nick'

import os

from django.core.management.base import BaseCommand, CommandError
from hydro import models, tasks
from Hydroinformatics import settings


class Command(BaseCommand):
	args = ''
	help = 'Tells Celery to process photos'

	def handle(self, *args, **options):
		photos = models.Image.objects.filter(is_processed=False)
		exif_registry = {}
		print "Adding images to processing queue"
		for photo in photos:
			tasks.process_image.delay(photo.pk, exif_registry)  # set up processing