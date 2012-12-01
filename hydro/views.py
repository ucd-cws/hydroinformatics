# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import Context, Template, loader, TemplateDoesNotExist, RequestContext
from django.template.loader import render_to_string
from django.core import exceptions

from Hydroinformatics import settings
import models
#import utils

import simplejson
#import compile_less # we want to autocompile less scripts on load

def log(msg):
	# 	TODO: needs to be fized by the time we go live

	print msg


def home(request):
	if settings.AUTOCOMPILE_LESS:
		pass
		#compile_less.compile_less(dirs = settings.STATICFILES_DIRS)

	template = loader.get_template("index.django")
	cont = RequestContext(request,{})
	return HttpResponse(template.render(cont))