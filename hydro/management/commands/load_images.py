__author__ = 'nrsantos'

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from hydro import models
from Hydroinformatics import settings


class Command(BaseCommand):
	args = 'A single site code to upload the images to'
	help = 'Loads images in bulk. Saves us writing an interface for now'

	def handle(self, *args, **options):
		site = args[0]
		if not site:
			raise ValueError("ERROR: Must specify a site on the command line")

