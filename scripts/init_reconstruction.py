import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fossilhunter.settings")
django.setup()

from app import models

info_object = models.ReconstrucationModel.objects.create(
    specie_id=2,
    modelpath='https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/test2.glb',
)