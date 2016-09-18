from django import forms
from django.forms import ModelForm 
from sigmauser.models import UserProfile
from exploredata.models import timeseriesmodel
from django.contrib.auth.models import User




class CreateTSForm(ModelForm):
    class Meta:
        model=timeseriesmodel
        fields={'modelname', 'modeldescription','datasetid', 'modeldocumentation'}



class WorkSpaceSpec(forms.Form):
    indepVar=forms.ChoiceField(label='indepVar')
    depVar=forms.ChoiceField(label='depVar')
    modeltype=forms.ChoiceField(choices=((1,'ARIMAX'),(2,'OLS'),(3,'VAR')) )
    AR=forms.IntegerField(label='AR',min_value=0,max_value=32)
    MA=forms.IntegerField(label='MA',min_value=0,max_value=32)
    I=forms.IntegerField(label='I',min_value=0,max_value=32)
    startdate=forms.DateTimeField(label='startdate')
    enddate=forms.DateTimeField(label='enddate')
    

       
class RunTSForm(ModelForm):
    class Meta:
        model=timeseriesmodel
        fields={'modelname', 'modeldescription', 'modeldocumentation'}

    

        



