# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader_environments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='runtimeenvironment',
            name='port',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Port'),
        ),
    ]