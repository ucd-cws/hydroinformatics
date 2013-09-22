__author__ = 'nrsantos'

from fabric.api import *
from fabric.operations import *
try:
	import fabfile_passwords as pw  # separate file so we can commit this without it
except:
	pass

import os

all_machines_commands = (
	"pip install virtualenv",
	"virtualenv hydroinformatics",
	"source bin/activate", 
	"pip install arrow",
	"pip install ulmo",
	"pip install PIL",
	"pip install django-imagekit",
	"pip install simplejson",
	"pip install Pysolar",
	"pip install wand",
	"pip install usgs-api",
)

env.hosts = ['nick@localhost:31']
env.passwords = pw.pws

def test():
	local("./manage.py test hydro")

def commit_and_push():
	test()
	#local("hg")
	local("hg push")

def setup_local():
	for command in all_machines_commands:
		local(command)

def setup_all():
	for command in all_machines_commands:
		run(command)

def setup_linux():
	setup_all()
	setup_debian()

def setup_debian():
	"""
		Sets up a full linux django stack, based on http://www.apreche.net/complete-single-server-django-stack-tutorial/
		Further config should be done, but it does all the installs
	"""
	local("sudo add-apt-repository ppa:mercurial-ppa/releases")  # add mercurial repo first
	local("sudo apt-get update")
	local("sudo apt-get dist-upgrade")
	local("sudo apt-get autoremove")
	local("sudo reboot")

def setup_debian_continued():
	# basic tools
	local("sudo apt-get install mercurial")
	local("sudo apt-get install python-pip")
	setup_local()

def setup_windows():
	setup_all()