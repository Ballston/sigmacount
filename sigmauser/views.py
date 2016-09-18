from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

from django.template import loader, RequestContext 
from django.contrib.auth.decorators import login_required

from sigmauser.forms import UserForm, UserProfileForm, UserLoginForm
from sigmauser.models import  UserProfile

from exploredata.models import datasets, timeseriesmodel
from django.contrib.auth.models import User


from exploredata import owndatasets
# def home(request):
#     
#     return render(request, 'builder/dataexplore.html', {'form_login': form})
def createproject(request, projecttype):
    if projecttype=='exploredata':
        return HttpResponse('<h1>exploredata</h1>')
    if projecttype=='tsbuild':
        return HttpResponse('<h1>tsbuild</h1>')
    else:
        return HttpResponse('<h1>projecttype</h1>')

    
    
def logoutview(request):
    logout(request)
    print 'trying to log out'
    return HttpResponseRedirect('/')

def homepage(request):
    if request.user.is_authenticated():
        dsets=datasets.objects.filter(user=request.user)
        tsmsets=timeseriesmodel.objects.filter(user=request.user)
        #tsmodels=tsmodels.objects.filter(user=request.user)
        if len(owndatasets)<1:
            for i in dsets:
                owndatasets.append(i.datasetid)

        return render( request, 'sigmauser/home.html', {'nothing': 'nothing' , 'dsets': dsets, 'tsmsets': tsmsets})
        
    else:
        print 'Hello \n'
        return HttpResponseRedirect('/sigmauser/login/')

def loginview(request):
    print 'I aam in Loginview \n'
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        print 'Post was success \n'
        
        user=authenticate(username=username,password=password)
        login(request, user)
        if user:
            if request.user.is_authenticated():
                print 'User was validated'
                return HttpResponseRedirect('/')
        else:
            login_form=UserLoginForm()
            
    else:
         login_form=UserLoginForm()

    return render( request, 'sigmauser/home.html', {'login_form': login_form})


def register(request):
    context=RequestContext(request)
    
    registered=False
    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)
       
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            
            user.set_password(user.password)
            user.save()
            
            profile=profile_form.save(commit=False)
            profile.user=user
            
            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']
            
            profile.save()
            
            registered=True
            
        else:
            print user_form.errors, profile_form.errors
            
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
            
            
    return render(request,  'sigmauser/register.html', {'user_form' : user_form, 'profile_form': profile_form, 'registered': registered} )