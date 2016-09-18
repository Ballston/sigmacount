# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2016-09-07 02:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exploredata', '0002_auto_20160829_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='tsmodelstats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stat', models.CharField(db_column='parameter', max_length=32)),
                ('value', models.FloatField(blank=True, db_column='value', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tsmodelvalues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.CharField(db_column='parameter', max_length=32)),
                ('parameter_type', models.CharField(db_column='parameter_type', max_length=4)),
                ('value', models.FloatField(blank=True, db_column='value', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tsmodelworkflow',
            fields=[
                ('workflowid', models.AutoField(db_column='workflowid', primary_key=True, serialize=False)),
                ('workflownotes', models.TextField(db_column='workflownotes', max_length=256)),
                ('stardatetime', models.DateTimeField(db_column='startdatetime')),
                ('enddatetime', models.DateTimeField(db_column='enddatetime')),
                ('estimated', models.BinaryField(db_column='estimated')),
                ('modeltype', models.CharField(db_column='modeltype', max_length=8)),
                ('tsmodelid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exploredata.timeseriesmodel')),
            ],
        ),
        migrations.AddField(
            model_name='tsmodelvalues',
            name='workflowid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exploredata.tsmodelworkflow'),
        ),
        migrations.AddField(
            model_name='tsmodelstats',
            name='workflowid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exploredata.tsmodelworkflow'),
        ),
    ]
