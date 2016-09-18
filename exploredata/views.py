##
#Descrpition: This file contain all of the views for the explore data application
#
##
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from exploredata.forms import LoadDataForm, PlotData

import pandas as pd
from pandas import DataFrame
import pandas.io.data

import datetime

from .models import timeseries, datasets
from exploredata import owndatasets
 
def Load(request):
    print owndatasets
    if request.method=='POST':
        loaddata_form = LoadDataForm(request.POST, request.FILES)
        if loaddata_form.is_valid:
            df = pd.read_csv(request.FILES['ff'], index_col='Date', parse_dates=True)
            dset=datasets(dataname=request.POST.get('sn'), user=request.user)
            dset.save()
            for col in  df.columns:
                for i in  range(0,len(df[col])-1 ):
                    ts=timeseries(datasetid=dset, seriesname=col,value=df[col][i],date=df.index[i])
                    ts.save()
                
            #print loaddata_form.sn
           # print dir(request.POST)
            #print request.POST.get('sn')
            #print request.user.username
            #print dset.datasetid
            print dir(df)
            #print df.columns
    else:
        loaddata_form=LoadDataForm()
   
    return render(request,'exploredata/loaddata.html',{'loaddata_form': loaddata_form})


def ExploreData(request,dataset_id):
    #Check if the dataset belongs to the user
    variables=timeseries.objects.filter(datasetid_id=dataset_id).values('seriesname').distinct()
    df=pd.DataFrame()
    for v in variables:
        series=timeseries.objects.filter(datasetid_id=dataset_id,seriesname=v['seriesname']).values('date','value')
        index=[]
        value=[]
        for s in series:
            index.append(s['date'])
            value.append(s['value'])
        
        seriestoinsert=pd.Series(value,index=index)
        df[v['seriesname']]=seriestoinsert
        #print seriestoinsert
            
    #print dataset_id
    #print variables
    print df.columns
    existing_results=[]
    
    plotform=PlotData()
    return render(request, 'exploredata/exploredata.html', {'existing_results': existing_results, 'plotform':plotform})

    

    
    