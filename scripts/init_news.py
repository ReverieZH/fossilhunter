import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fossilhunter.settings")
django.setup()

from app import models

for i in range(1, 5):
    info_object = models.NewsList.objects.create(
        title="test{0}".format(i),
        content='新系统开启test{0}'.format(i),
    )