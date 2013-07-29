'''
Created on Mar 3, 2012

@author: Nick
'''

import common
from common import log
use_in_memory = True  # a configuration flag that sets whether or not to use the in_memory workspace for temp files
temp_datasets = []  # a registry for temp datasets so that you can always clean up if you want to

__all__ = ['common']


def isiterable(item):
	"""tests whether an object is iterable

	TODO: May be replacable with just return hasattr() - not super useful, but prevents needing to remember the syntax and names
	"""
	if hasattr(item, '__iter__'):
		return True
	else:
		return False

