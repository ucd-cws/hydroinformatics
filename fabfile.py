__author__ = 'nrsantos'

from fabric.api import *
from fabric.operations import *
try:
	import fabfile_passwords as pw  # separate file so we can commit this without it
except:
	pass

import os

env.hosts = ['nick@localhost:31']
env.passwords = pw.pws

def test():
	local("./manage.py test hydro")

def commit_and_push():
	test()
	#local("hg")
	local("hg push")

def setup_linux():
	setup_debian()

def setup_debian():
	"""
		Sets up a full linux django stack, based on http://www.apreche.net/complete-single-server-django-stack-tutorial/
		Further config should be done, but it does all the installs
	"""
	run("sudo add-apt-repository ppa:mercurial-ppa/releases")  # add mercurial repo first
	run("sudo apt-get update")
	run("sudo apt-get dist-upgrade")
	run("sudo apt-get autoremove")
	run("sudo reboot")

	# basic tools
	run("sudo apt-get install mercurial")

def setup_windows():
