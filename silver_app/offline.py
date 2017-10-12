import django
from django.conf import settings

settings.configure(DEBUG=True)
django.setup()
