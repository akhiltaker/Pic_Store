# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-20 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_album_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='picture',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='picture',
            name='pic_file',
            field=models.FileField(default='', upload_to=''),
        ),
    ]