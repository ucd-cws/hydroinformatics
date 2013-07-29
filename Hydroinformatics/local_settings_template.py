__author__ = 'nrsantos'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_VHOST = "/"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'hydro.sqlite3',  # Or path to database file if using sqlite3.
		'USER': '',  # Not used with sqlite3.
		'PASSWORD': '',  # Not used with sqlite3.
		'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',  # Set to empty string for default. Not used with sqlite3.
	}
}