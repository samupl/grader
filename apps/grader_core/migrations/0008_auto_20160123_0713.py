# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-23 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader_core', '0007_auto_20160109_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='arguments',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Arguments'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='repository_type',
            field=models.CharField(choices=[('svn', 'Subversion (SVN)'), ('hg', 'Mercurial (hg)'), ('git', 'GIT')], max_length=24, verbose_name='Type'),
        ),
    ]
