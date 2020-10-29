from . import *
from selenium import webdriver

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '',
    },
}

SELENIUM_WEBDRIVERS = {
    'default': {
        'callable': webdriver.Chrome,
        'args': (),
        'kwargs': {},
    },
    'firefox': {
        'callable': webdriver.Firefox,
        'args': (),
        'kwargs': {},
    },
}
