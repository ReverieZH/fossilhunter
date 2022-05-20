# Generated by Django 3.2.13 on 2022-05-13 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20220513_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentUser', to='app.userinfo', verbose_name='用户ID'),
        ),
    ]
