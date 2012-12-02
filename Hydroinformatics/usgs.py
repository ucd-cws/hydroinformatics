__author__ = 'nicksantos'

"""
	Handles all interfacing with USGS, with the goal of making (parts) of their JSON
	API available to Python as native objects
"""

import pandas
import urllib
import urllib2
import json

class gage():
	def __init__(self, station_id = None, time_period = "P7D", url_params = {}):

		self.station_id = station_id
		self.time_series = None
		self.time_period = time_period
		self.url_params = url_params # optional dict of params - url key value pairs passed to the api

		self._data_frame = None
		self._json_string = None
		self._base_url = "http://waterservices.usgs.gov/nwis/iv/"

	def check_params(self, params = ('station_id',)):
		"""
			Makes sure that we have the base level of information necessary to run a query
			to prevent lazy setup errors
		"""

		for param in params:
			if self.__dict__[param] is None:
				raise AttributeError("Required attribute %s must be set before running this method" % param)

	def retrieve(self):
		"""
			runs the relevant private methods in sequence

		"""

		# makes sure that the user didn't forget to set something after init
		self.check_params()

		self._retrieve_data()
		self._json_to_dataframe()

	def _retrieve_data(self):
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

		self._json_data = json.loads(self._json_string)

	def _json_to_dataframe(self):
		"""
			converts the json to a pandas data frame
		"""

		self._time_series_only = self._json_data['value']['timeSeries'][0]['values'][0]['value']

		self._data_frame = pandas.DataFrame(self._time_series_only)


		pass

	def _merge_with_existing(self):
		"""
			if we execute a request when we already have data, this method attempts
			to merge the two datasets into a single time series so you can effectively
			execute a partial query and then go further if need be
		"""
		pass