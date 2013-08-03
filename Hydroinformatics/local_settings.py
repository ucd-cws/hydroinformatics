__author__ = 'nrsantos'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BROKER_H = "localhost"
BROKER_P = 5672
BROKER_VH = "/"
BROKER_U = "guest"
BROKER_PASS = "guest"
BROKER_URL = 'amqp://%s:%s@%s:%s/%s' % (BROKER_U, BROKER_PASS, BROKER_H, BROKER_P, BROKER_VH)

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