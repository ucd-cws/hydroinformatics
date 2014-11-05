__author__ = 'nrsantos'

class IFormatterRegistry(type): # Build a metaclass that inherits from "type" - it ends up being another intermediary that performs function registration.
	plugins = []
	plugins_by_name = {}

	def __init__(cls, name, bases, attrs):
		#super(IFormatterRegistry, cls).__init__()


	def _get_process_entry_hook(self):if name != 'IFormatter':  # if it's not the base class
			IFormatterRegistry.plugins.append(cls) # plugins is already an object since it's built in the class, not in an instance
			IFormatterRegistry.plugins_by_name[cls.__name__] = cls # add it to the index

class IFormatter(object):
	__metaclass__=IFormatterRegistry

	def __init__(self, data_series=list(), photo_series=list()):
		self.data_series = data_series
		self.photo_series = photo_series

		"""
			Process entry hook is the hook a plugin uses to take over for the full processing of a video
		"""
		return None