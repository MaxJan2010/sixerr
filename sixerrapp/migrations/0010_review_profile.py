# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sixerrapp', '0009_auto_20160709_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sixerrapp.Profile'),
            preserve_default=False,
        ),
    ]