# Generated by Django 2.1.15 on 2021-01-25 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210117_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciesguide',
            name='picture',
            field=models.CharField(max_length=640, verbose_name='图片'),
        ),
    ]