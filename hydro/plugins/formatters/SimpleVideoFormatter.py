__author__ = 'nrsantos'

from hydro.plugins.formatters import IFormatter

from celery import task

class SimpleVideoFormatter(IFormatter):
	"""
		Plugin is automatically registered by its use of the IFormatter class as its base
	"""

	def __init__(self):
		pass

	def _get_process_entry_hook(self):
		return self.entry  # this form may be unnecessary because we aren't returning different functions based on params, but we'll stay consistent

	def entry(self):
		pass
		self.generate(None)

	def generate(self, frames):
		"""

		:param frames: the full path to the images to generate into a video
		"""
		pass
	"""
		create a method in images.py
			write_video_from_frames
			takes dimensions and a quality parameter
			takes parameter of a list of images
			names video based upon plugin, date and time

		# get a tempfile name
		# if linux, name it .sh
		# if windows, name it .bat
		# else, platform not supported

		write file with cat image_list | ffmpeg -f image2pipe -c:v mjpeg -i - -b:v 10000k {output_filename.mp4}
		other possible command ffmpeg -r {framerate} -i "%d.jpg" -b:v {bitrate in bytes} {outputfilename}
		if linux, can use glob format to do *.jpg - doesn't require sequential image names

		ffmpeg path should be in local settings
		output filename should be attached to a video object so it gets moved to the correct location when saved
		this generate function probably doesn't need to be a task, but the output item does.

		Call it from here and use .delay()
	"""