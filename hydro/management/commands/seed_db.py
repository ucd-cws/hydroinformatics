__author__ = 'Nick'

import csv
import os
import sys

from django.core.management.base import BaseCommand, CommandError
from hydro import models
from Hydroinformatics import settings


class Command(BaseCommand):
	args = ''
	help = 'Seeds the database with some basic information after it has been nuked'

	def handle(self, *args, **options):
		self.data_folder = os.path.join(settings._current_dir, "supplementary")
		self.read_rivers()
		self.seed()
		self.stdout.write("Done - running this again will double up the data\n")
		self.exit()

	def read_rivers(self):
		self.csv_file = open(os.path.join(self.data_folder, "ca_stations.csv"), 'rb')
		self.rivers = csv.DictReader(self.csv_file)

	def seed(self):
		added_rivers = {}
		for gage_row in self.rivers:  # for every row
			if gage_row['river'] and gage_row['river'] not in added_rivers:  # if we don't already have a river
				try:
					river = models.River.objects.get(name=gage_row['river'])
				except:
					print "Adding River: %s" % gage_row['river']
					t_river = models.River(name=gage_row['river'])  # make one
					added_rivers[gage_row['river']] = True  # store that we've added it
					t_river.save()  # save it

			if gage_row['river']:
				# if it's assigned to a river, then we want to add it
				print "Adding station: %s" % gage_row['station_nm']
				t_station = models.Station(
					usgs_id=gage_row['site_no'],
					name=gage_row['station_nm'],
					river=models.River.objects.get(name=gage_row['river']),
					lat=gage_row['dec_lat_va'],
					lon=gage_row['dec_long_va'],
				)
				t_station.save()

	def exit(self):
		self.csv_file.close()