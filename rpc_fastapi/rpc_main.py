import django
import os 
import sys
sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from apps.home.models import AC
print(AC.objects.all())
