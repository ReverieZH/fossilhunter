import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fossilhunter.settings")
django.setup()

from app import models

for i in range(1, 5):
    info_object = models.FossilPicture.objects.create(
        picturepath='https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/testpicture01.jpg',
        picturelocation='西北大学',
        species_id=i+4,
        document='00000',
        reconstruction='000'

    )