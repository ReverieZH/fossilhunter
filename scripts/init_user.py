import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fossilhunter.settings")
django.setup()

from app import models

for i in range(1, 2):
    info_object = models.UserInfo.objects.create(
        nickname='Leo Regulus',
        usericon='0000',
        status='学生',
        institution='西北大学',

    )