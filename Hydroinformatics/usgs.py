__author__ = 'nicksantos'

"""
	Handles all interfacing with USGS, with the goal of making (parts) of their JSON
	API available to Python as native objects
"""

import pandas

class usgs_gage():
	def __init__(self, station_id = None):

		self.station_id = station_id
		self.time_series = []

	def