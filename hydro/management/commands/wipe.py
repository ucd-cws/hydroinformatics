__author__ = 'Nick'

import os

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from hydro import models
from Hydroinformatics import settings


class Command(BaseCommand):
	args = ''
	help = 'Resets everything - deletes the sqlite database, makes a new one, syncs it and seeds it'

	def handle(self, *args, **options):
		db_path = os.path.join(settings._current_dir, "hydro.sqlite3")
		print "deleting %s" % db_path
		try:
			os.remove(db_path)
		except WindowsError:
			print "Couldn't delete database - it may not exist"
		call_command('syncdb', interactive=False)
		call_command('seed_db', interactive=False)
		call_command('process_images', interactive=False)

