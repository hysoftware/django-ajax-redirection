'''
Dummy settings
'''

DEBUG = True
SECRET_KEY = "secret"
DATABASES = {
    'default': {
        'ENGINE': ('django.db.backends.dummy'),
        'NAME': "hysoft.db"
    }
}
STATIC_URL = '/static/'
