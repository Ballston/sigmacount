from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from sigmauser.models import project

class datasets(models.Model):
    datasetid=models.AutoField(db_column='datasetid',primary_key=True)
    dataname=models.CharField(db_column='dataname',null=True,blank=True, max_length=32)
    #projectid=models.ForeignKey(project, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    
class seriesnames(models.Model):
    datasetid=models.ForeignKey(datasets, on_delete=models.CASCADE)
    seriesname=models.CharField(db_column='seriesname',null=True,blank=True, max_length=32)
    description=models.CharField(db_column='description',null=True,blank=True, max_length=256)
    

class timeseries(models.Model):
    datasetid=models.ForeignKey(datasets, on_delete=models.CASCADE)
    seriesname=models.CharField(db_column='seriesname',null=True,blank=True, max_length=32)
    value=models.FloatField(db_column='value',null=True,blank=True)
    date=models.DateTimeField(db_column='datetime',null=False)
    
    def wert(self):
        return {'seriesname': self.seriesname, 'value': self.value}
    

def generate_filename(tsmodelid,filename):
    url="files/users/%s/%s" % (tsmodelid,filename)
    return url 
    
class timeseriesmodel(models.Model):
    #Thi table conataing information about the model
    tsmodelid=models.AutoField(db_column='tsmodelid',primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    datasetid=models.ForeignKey(datasets, on_delete=models.CASCADE)
    modelname=models.CharField(db_column='modelname', max_length=32)
    modeldescription=models.TextField(db_column='modeldescription',max_length=256)
    modeldocumentation=models.FileField(upload_to=generate_filename)
    
class tsmodelworkflow(models.Model):
    #As the user is working on creating a model the process flow is retained
    #to capture different versions of the model
    tsmodelid=models.ForeignKey(timeseriesmodel, on_delete=models.CASCADE)
    workflowid=models.AutoField(db_column='workflowid',primary_key=True)
    workflownotes=models.TextField(db_column='workflownotes',max_length=256)
    stardatetime=models.DateTimeField(db_column='startdatetime')
    enddatetime=models.DateTimeField(db_column='enddatetime')
    estimated=models.BinaryField(db_column='estimated')
    modeltype=models.CharField(db_column='modeltype', max_length=8)
    AR=models.IntegerField(db_column='AR',default=0)
    MA=models.IntegerField(db_column='MA',default=0)
    I=models.IntegerField(db_column='I',default=0)
    
    
class tsmodelvalues(models.Model):
    #The parameters of the model in each itteration of the work flow are saved in this table
    workflowid=models.ForeignKey(tsmodelworkflow, on_delete=models.CASCADE)
    parameter=models.CharField(db_column='parameter', max_length=32)
    parameter_type=models.CharField(db_column='parameter_type',max_length=4)
    value=models.FloatField(db_column='value',null=True, blank=True)
    
class tsmodelstats(models.Model):
    workflowid=models.ForeignKey(tsmodelworkflow, on_delete=models.CASCADE)
    stat=models.CharField(db_column='parameter', max_length=32)
    value=models.FloatField(db_column='value',null=True,blank=True)

    
    
