__author__ = 'nrsantos'

# import os
# import imp

# import formatters

# __all__ = ["formatters"]


# def discover(folders):
	# print "Discovering plugins in %s" % folders
	# for folder in folders:
		# for filename in os.listdir(folder):
			# modname, ext = os.path.splitext(filename)
			# if ext == '.py':
				# l_file, path, descr = imp.find_module(modname, [folder])
				# if file:
					# # Loading the module registers the plugin in IPluginRegistry
					# mod = imp.load_module(modname, l_file, path, descr)
	# print "discovered %s" % (formatters.IFormatterRegistry.plugins)
	# return formatters.IFormatterRegistry.plugins