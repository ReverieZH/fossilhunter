import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fossilhunter.settings")
django.setup()

from app import models

info_object = models.FossilFamily.objects.create(
    fossil_id=2,
    user_id=5,
)