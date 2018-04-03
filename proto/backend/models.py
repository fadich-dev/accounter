import sys
import os
import django


sys.dont_write_bytecode = True
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# Import your models for use in your script
from backend.orm.models import *
