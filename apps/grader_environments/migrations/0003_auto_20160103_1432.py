# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 14:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grader_environments', '0002_runtimeenvironment_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuntimeEnvironmentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='runtimeenvironment',
            name='group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='grader_environments.RuntimeEnvironmentGroup'),
            preserve_default=False,
        ),
    ]
