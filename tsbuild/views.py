##
#Description: This file contains all of the views used in tsbuild application
#
##
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from tsbuild.forms import CreateTSForm, WorkSpaceSpec
from exploredata.models import datasets, timeseriesmodel,tsmodelworkflow,tsmodelvalues,timeseries, tsmodelstats

import os
import datetime
import pandas
import numpy

import matplotlib.pyplot as plt
import statsmodels.api as sm

import common

from common import modeler

#Create a TS project

def Createts(request):
    dsets=datasets.objects.filter(user=request.user)
    dsets_choices=[]
    for singleset in dsets:
        dsets_choices.append((singleset.datasetid,str(singleset.dataname)))
        
    if request.method=='POST':
        createts_form=CreateTSForm(request.POST,request.FILES)
        createts_form.fields['datasetid'].choices=dsets_choices
        
        if createts_form.is_valid():
            print('Attempting to save model')
            createdmodel=timeseriesmodel(user=request.user,
                                         modelname=request.POST.get('modelname'),
                                         modeldescription=request.POST.get('modeldescription'),
                                         datasetid=datasets(datasetid=request.POST.get('datasetid'))
                                         )
            #createdmodel.modeldocumentation=request.FILES.get('modeldocumentation')
            
            print('datasetid type \n')
            print(request.POST.get('datasetid'))
            createdmodel.save()
            
            #create first workspace for the model
            workflow=tsmodelworkflow(stardatetime=datetime.datetime(2010,1,1),
                                       enddatetime=datetime.datetime(2016,1,1),
                                       modeltype=1,
                                       AR=0,
                                       I=0,
                                       MA=0,
                                       tsmodelid=createdmodel
                                       )
            workflow.save()
            
            #Prepare location for saving
            os.mkdir('files/%s/' % (workflow.tsmodelid.tsmodelid) )
            os.mkdir('files/%s/%s/' % (workflow.tsmodelid.tsmodelid,workflow.workflowid) )
            
            myfile = request.FILES.get('modeldocumentation')
            fs = FileSystemStorage()
            filename = fs.save('files/%s/%s' % (workflow.tsmodelid.tsmodelid,myfile.name),myfile)
            uploaded_file_url = fs.url(filename)
            createdmodel.modeldocumentation=uploaded_file_url
            createdmodel.save()
            
    else:
        createts_form=CreateTSForm()
        createts_form.fields['datasetid'].choices=dsets_choices
    
    return render(request,'tsbuild/createts.html',{'createts_form': createts_form})
    
def ModelHomePage(request,tsmodelid):
    tsmodel=timeseriesmodel(tsmodelid=tsmodelid)
    workspaces=tsmodelworkflow.objects.filter(tsmodelid=tsmodelid).values('workflowid')
    workspaces_list=[]
    for i in workspaces:
        workspaces_list.append(i['workflowid'])
    print(workspaces)
    return render(request,'tsbuild/modelhomepage.html',{'workspaces':workspaces_list, 'tsmodelid':tsmodelid})

def AddWorkSpace(request,tsmodelid):
    tsmodel=timeseriesmodel(tsmodelid=tsmodelid)
    workflow=tsmodelworkflow(stardatetime=datetime.datetime(2010,1,1),
                                       enddatetime=datetime.datetime(2016,1,1),
                                       modeltype=1,
                                       AR=0,
                                       I=0,
                                       MA=0,
                                       tsmodelid=tsmodel
                                       )
    workflow.save()
    tsworkspaceid=workflow.workflowid
    os.mkdir('files/%s/%s/' % (workflow.tsmodelid.tsmodelid,workflow.workflowid) )
    
    return HttpResponseRedirect('/tsbuild/workspace/%s/%s/' % (str(tsmodelid),str(tsworkspaceid)))
    

class WorkSpaceClass(object):
    depVar=[];
    indepVar=[];
    modeltype=1;
    AR=0;
    MA=0;
    I=0;
    startdate=datetime.datetime(2010,1,1)
    enddate=datetime.datetime(2016,1,1)
    data=pandas.DataFrame()
    
    fit=[]
    workspacespec_form=WorkSpaceSpec()
    estimated=False
    
    
    def Save(self,request,tsmodelid,tsworkspaceid):
        modelid=timeseriesmodel(tsmodelid=tsmodelid)
        workspaceid=tsmodelworkflow(workflowid=tsworkspaceid)
        instance=tsmodelworkflow.objects.get(workflowid=tsworkspaceid)
        print('instance')
        print(instance.stardatetime)
        instance.stardatetime=self.startdate
        instance.enddatetime=self.enddate
        instance.modeltype=self.modeltype
        instance.AR=self.AR
        instance.I=self.I
        instance.MA=self.MA
        instance.save()
        
        return HttpResponseRedirect('/tsbuild/workspace/%s/%s' % (str(tsmodelid),str(tsworkspaceid)))
             
    def WorkSpaceConstruct(self,request,tsmodelid,tsworkspaceid):
        
        
        dataset_id=timeseriesmodel.objects.filter(tsmodelid=tsmodelid).values('datasetid')
        
        #Get list of all workspaces associated with the model
        allworkspaces=tsmodelworkflow.objects.filter(tsmodelid=tsmodelid).values('workflowid')
        
        #Get workflow properties
        instance=tsmodelworkflow.objects.filter(workflowid=tsworkspaceid)
        
        #For the current workspace get the list of all parameter values that were saved
        workspacevalues=tsmodelvalues.objects.filter(workflowid=tsworkspaceid)

        self.AR=instance.values('AR')[0]['AR']
        self.MA=instance.values('MA')[0]['MA']
        self.I=instance.values('I')[0]['I']
        
        self.stardate=instance.values('stardatetime')[0]['stardatetime']
        self.enddate=instance.values('enddatetime')[0]['enddatetime']
        self.modeltype=instance.values('modeltype')[0]['modeltype']
        
        
        #For the current workspace get the all of the statistics
        workspacestats=tsmodelstats.objects.filter(workflowid=tsworkspaceid)
        
        
        
        variables=timeseries.objects.filter(datasetid_id=dataset_id).values('seriesname').distinct()
        variables_choicelist=[]
        for i in variables:
            variables_choicelist.append((i['seriesname'],i['seriesname']))
            
        self.workspacespec_form.fields['depVar'].choices=variables_choicelist
        self.workspacespec_form.fields['indepVar'].choices=variables_choicelist
        self.workspacespec_form.fields['modeltype'].initial=self.modeltype
        self.workspacespec_form.fields['AR'].initial=self.AR
        self.workspacespec_form.fields['MA'].initial=self.MA
        self.workspacespec_form.fields['I'].initial=self.I
        self.workspacespec_form.fields['startdate'].initial=self.startdate
        self.workspacespec_form.fields['enddate'].initial=self.enddate
        
        if len(self.depVar)>0:
            self.workspacespec_form.fields['depVar'].initial=self.depVar[0]
        
        #print(self.workspacespec_form.fields['modeltype'].initial)
        
        print(variables[0])
        print(self.indepVar)
        return render(request,'tsbuild/workspace.html',{'workspacespec_form': self.workspacespec_form,
                                                         'tsmodelid': tsmodelid,
                                                         'tsworkspaceid':tsworkspaceid,
                                                         'spec': self} )
    
    def AddIndependentVar(self,request,tsmodelid,tsworkspaceid):
        print('Attempting to add independent variable\n')
        if request.method=='POST':
            #workspacespec_form=WorkSpaceSpec(request.POST)
            #workspacespec_form.
            #check check if variable is already in the list of independent variable if not append the list
            if self.indepVar.count(request.POST.get('indepVar'))>0:
                #print('Skipping, the variable is already in the list')
                pass
            else:
                self.indepVar.append(request.POST.get('indepVar'))
            
            #print('The independent set is\n')
            #print(self.indepVar)
        #return render(request,'tsbuild/workspace.html',{'workspacespec_form': self.workspacespec_form, 'tsmodelid': tsmodelid, 'spec': self} )
        return HttpResponseRedirect('/tsbuild/workspace/%s/%s' % (str(tsmodelid),str(tsworkspaceid)))
    
    def SetSpecifications(self,request,tsmodelid,tsworkspaceid):
        if request.method=='POST':
            self.AR=request.POST.get('AR')
            self.I=request.POST.get('I')
            self.MA=request.POST.get('MA')
            self.depVar=[] #need to make sure a list of dep vars is not created 
            self.depVar.append(request.POST.get('depVar'))
            self.modeltype=request.POST.get('modeltype')
            self.startdate=request.POST.get('startdate')
            self.enddate=request.POST.get('enddate')
        
        #return HttpResponseRedirect('/tsbuild/workspace/%s/%s' % (str(tsmodelid),str(tsworkspaceid)))
        return self.Save(request,tsmodelid,tsworkspaceid)
    
    def getseries(self,datasetid,seriesname):
        series=timeseries.objects.filter(datasetid=datasetid,seriesname=seriesname).values('date','value')
        index=[]
        value=[]
        for s in series:
            index.append(s['date'])
            value.append(s['value'])
        
        pdseries=pandas.Series(value,index=index)
        
        return pdseries
        
    def prepdata(self,tsmodelid):
        dataset_id=timeseriesmodel.objects.filter(tsmodelid=tsmodelid).values('datasetid')
        print(dataset_id)
        #load all of the independent variables into the pandas 
        for var in self.indepVar:
            seriestoinsert=self.getseries(dataset_id,var)
            self.data[var]=seriestoinsert
        #load dependent variable into the pandas
        print(self.depVar)
        seriestoinsert=self.getseries(dataset_id,self.depVar[0])
        self.data[self.depVar[0]]=seriestoinsert
        self.data=self.data[self.startdate:self.enddate]
        return 0
    
    def RunEstimation(self,request,tsmodelid,tsworkspaceid):
        self.data=pandas.DataFrame()
        self.prepdata(tsmodelid)
        print(self.data)
        ig=lambda x:x
        g=lambda x:x
        print(self.depVar[0])
        test=modeler.ModelClass(data=self.data,startdate=self.startdate,enddate=self.enddate, dependent=self.depVar[0],exogenous=self.indepVar ,transform=g,inverstransform=ig)
        test.setmodel(AR=int(self.AR),I=int(self.I),MA=int(self.MA))
        
        
        test.estimate()
        self.fit=test.fit
        print test.fit.summary()
        #return HttpResponseRedirect('/tsbuild/workspace/%s/%s' % (str(tsmodelid),str(tsworkspaceid)))
        confint0=self.fit.conf_int()[0]
        confint1=self.fit.conf_int()[1]
        
        self.SaveValues(tsmodelid,tsworkspaceid,test.fit)
        
        
        sm.qqplot(test.fit.resid)
        plt.savefig('files/%s/%s/qqplot_resid.png' % (tsmodelid, tsworkspaceid))
        
        return render(request,'tsbuild/arimaSummary.html', {'fit': self.fit, 'confint0':confint0, 'confint1':confint1} )
    
    def SaveValues(self,tsmodelid,tsworkspaceid,fit):
        workflowid=tsmodelworkflow(workflowid=tsworkspaceid)
        tsmodelvalues.objects.filter(workflowid=workflowid).delete()
        tsmodelstats.objects.filter(workflowid=workflowid).delete()
        
        tsmodelstats(workflowid=workflowid, stat='aic',value=fit.aic).save()
        tsmodelstats(workflowid=workflowid, stat='bic',value=fit.bic).save()
        tsmodelstats(workflowid=workflowid, stat='hqic',value=fit.hqic).save()
        #tsmodelvalues(workflowid=workflowid,)
        for i in range(0,len(fit.params)):
            tsmodelvalues(workflowid=workflowid, parameter=fit.params.index[i],
                           parameter_type='coef',value=fit.params[i]).save()
            tsmodelvalues(workflowid=workflowid, parameter=fit.params.index[i],
                           parameter_type='stde',value=fit.bse[i]).save()
            tsmodelvalues(workflowid=workflowid, parameter=fit.params.index[i],
                           parameter_type='tval',value=fit.tvalues[i]).save()
            tsmodelvalues(workflowid=workflowid, parameter=fit.params.index[i],
                           parameter_type='pval',value=fit.pvalues[i]).save()
            tsmodelvalues(workflowid=workflowid, parameter=fit.params.index[i],
                           parameter_type='c25',value=fit.conf_int()[0][i]).save()
            tsmodelvalues(workflowid=workflowid, parameter=fit.params.index[i],
                           parameter_type='c975',value=fit.conf_int()[1][i]).save()
        
        return 0

        
    def ClearSpecification(self,request,tsmodelid,tsworkspaceid):
        print('Clear Specifications \n')
        self.depVar=[]
        self.indepVar=[]
        self.modeltype=1
        self.AR=1
        self.MA=0
        self.I=0
        return HttpResponseRedirect('/tsbuild/workspace/%s/%s' % (str(tsmodelid),str(tsworkspaceid)))

WorkSpace=WorkSpaceClass()

    
