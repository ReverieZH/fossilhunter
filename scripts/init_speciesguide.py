import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fossilhunter.settings")
django.setup()

from app import models

for i in range(1, 3):
    info_object = models.SpeciesGuide.objects.create(
        speciesname='测试物种{0}'.format(i+4),
        specieslocation='1024',
        epoch='寒武纪',
        describe='三叶虫是距今5.6亿年前的寒武纪就出现的最有代表性的远古动物，是节肢动物的一种，全身明显分为头、胸、尾三部分，背甲坚硬，背甲为两条背沟纵向分为大致相等的三片——一个轴叶和两个肋叶，因此名为三叶虫。',
        picture=['https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/testpicture01.jpg', 'https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/testpicture01.jpg'],
        speciescover='https://wx-miniprogram-picture-1302593558.cos.ap-chengdu.myqcloud.com/testpicture02.jpg'

    )