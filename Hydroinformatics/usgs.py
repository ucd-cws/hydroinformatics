__author__ = 'nicksantos'

"""
	Handles all interfacing with USGS, with the goal of making (parts) of their JSON
	API available to Python as native objects
"""

import pandas
import urllib
import urllib2
import json

class usgs_gage():
	def __init__(self, station_id = None, time_period = "P7D", url_params = {}):

		self.station_id = station_id
		self.time_series = None
		self.time_period = time_period
		self.url_params = url_params # optional dict of params - url key value pairs passed to the api

		self._data_frame = None
		self._json_string = None
		self._base_url = "http://waterservices.usgs.gov/nwis/iv/"



	def retrieve(self):
		"""
			requests retrieves, and stores the json
		"""

		# add the relevant parameters into the dictionary passed by the user (if any
		self.url_params['format'] = "json"
		self.url_params['sites'] = self.station_id
		self.url_params['period'] = self.time_period

		# merge parameters into the url
		request_url = self._base_url + "?" + urllib.urlencode(self.url_params)

		# open the url and read in the json string to a private variable
		request = urllib2.Request(request_url)
		data_stream = urllib2.urlopen(request)
		self._json_string = data_stream.read()

		# TODO: run the string through json parser and save as self._json_data

	def json_to_dataframe(self):
		"""
			converts the json to a pandas data frame
		"""
		pass

	def merge_with_existing(self):
		"""
			if we execute a request when we already have data, this method attempts
			to merge the two datasets into a single time series so you can effectively
			execute a partial query and then go further if need be
		"""
		pass