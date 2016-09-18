from django import forms
from sigmauser.models import UserProfile
from django.contrib.auth.models import User


class LoadDataForm(forms.Form):
    sn=forms.CharField(max_length=32, label='seriesname' )
    ff=forms.FileField()

class PlotData(forms.Form):
    vartoplot=forms.MultipleChoiceField()