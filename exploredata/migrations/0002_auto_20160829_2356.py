# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-08-29 23:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import exploredata.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exploredata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='timeseriesmodel',
            fields=[
                ('tsmodelid', models.AutoField(db_column='tsmodelid', primary_key=True, serialize=False)),
                ('modelname', models.CharField(db_column='modelname', max_length=32)),
                ('modeldescription', models.TextField(db_column='modeldescription', max_length=256)),
                ('modeldocumentation', models.FileField(upload_to=exploredata.models.generate_filename)),
                ('datasetid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exploredata.datasets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='seriesnames',
            old_name='datasettid',
            new_name='datasetid',
        ),
        migrations.RenameField(
            model_name='timeseries',
            old_name='datasettid',
            new_name='datasetid',
        ),
    ]
