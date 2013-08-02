__author__ = 'Nick'

import csv
import os
import sys

from django.core.management.base import BaseCommand, CommandError

from hydro import models
from hydro import images
from hydro import tasks

from Hydroinformatics import settings
try:
	from code_library.common import utils2
except:
	from code_library_backup.common import utils2

class Command(BaseCommand):
	args = ''
	help = 'Seeds the database with some basic information after it has been nuked'

	def handle(self, *args, **options):
		self.data_folder = os.path.join(settings._current_dir, "supplementary")
		self.read_rivers()
		self.read_sites()
		self.read_cameras()
		self.read_photos()
		self.seed()
		self.stdout.write("Done - running this again will double up the data\n")
		self.exit()

	def read_rivers(self):
		self.csv_file = open(os.path.join(self.data_folder, "ca_stations.csv"), 'rb')
		self.rivers = csv.DictReader(self.csv_file)

	def read_sites(self):
		self.sites_csv_file = open(os.path.join(self.data_folder, "sites.csv"), 'rb')
		self.sites = csv.DictReader(self.sites_csv_file)

	def read_cameras(self):
		self.cameras_csv_file = open(os.path.join(self.data_folder, "cameras.csv"), 'rb')
		self.cameras = csv.DictReader(self.cameras_csv_file)

	def read_photos(self):
		self.photos = utils2.listdir_by_ext(os.path.join(self.data_folder, "sample_photos"), "JPG", full=True)

	def seed(self):
		self.seed_gages_and_rivers()
		self.seed_sites()
		self.seed_cameras()
		self.seed_photos()
		# TODO: This should export fixtures when it's done

	def seed_photos(self):

		cam = models.Camera.objects.get(name="Moultrie")
		for photo in self.photos:
			tp = models.Image(image=images.make_temp_photo(photo), camera=cam)  # assign the first camera to the image
			tp.save()
			tasks.process_image(tp.pk).delay()  # set up processing


	def seed_gages_and_rivers(self):
		added_rivers = {}
		print "seeding stations and rivers"
		for gage_row in self.rivers:  # for every row
			if gage_row['river'] and gage_row['river'] not in added_rivers:  # if we don't already have a river
				try:
					models.River.objects.get(name=gage_row['river'])  # this line is just to see if it exists, not to store it
				except:
					#print "Adding River: %s" % gage_row['river']
					t_river = models.River(name=gage_row['river'])  # make one
					added_rivers[gage_row['river']] = True  # store that we've added it
					t_river.save()  # save it

			if gage_row['river']:
				# if it's assigned to a river, then we want to add it
				#print "Adding station: %s" % gage_row['station_nm']
				t_station = models.Station(
					usgs_id=gage_row['site_no'],
					name=gage_row['station_nm'],
					river=models.River.objects.get(name=gage_row['river']),
					lat=gage_row['dec_lat_va'],
					lon=gage_row['dec_long_va'],
				)
				t_station.save()

	def seed_sites(self):
		print "seeding sites"
		for site in self.sites:
			try:
				river = models.River.objects.get(name=site['river'])
			except:
				print "ERROR: Couldn't look up river for site %s" % site['name']
				continue

			photo = images.make_temp_photo(os.path.join(self.data_folder, "site_photos", "%s.jpg" % site['name']))

			new_site = models.Site(
				name=site['name'],
				river=river,
				notes="imported via seed_db",
				representative_photo=photo,
				shortcode=site['shortcode']
			)

			new_site.save()
			#print "Added site %s" % site['name']

	def seed_cameras(self):
		print "seeding cameras"

		for cam in self.cameras:
			print "adding %s" % cam['name']
			new_camera = models.Camera(
				name=cam['name'],
				model_name=cam['model_name'],
				time_exif_field=cam['time_exif_field'],
				time_regex=cam['time_regex'],
				baro_exif_field=cam['baro_exif_field'],
				baro_regex=cam['baro_regex'],
				baro_units=cam['baro_units'],
				site_field=cam['site_field'],
				site_regex=cam['site_regex'],
			)

			if cam['has_baro'] == "1":
				new_camera.has_baro = True
			if cam['has_site'] == "1":
				new_camera.has_site = True
			if cam['photo'] and cam['photo'] != "":
				new_camera.representative_photo = images.make_temp_photo(os.path.join(self.data_folder, cam['photo']))
			new_camera.save()

	def exit(self):
		self.csv_file.close()
		self.sites_csv_file.close()
		self.cameras_csv_file.close()