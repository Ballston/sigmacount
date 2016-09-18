from django.conf.urls import url

from . import views

urlpatterns = [
    url( r'^$', views.Createts, name='Createts'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/(?P<tsworkspaceid>[0-9]+)/$' , views.WorkSpace.WorkSpaceConstruct, name='WorkSpace'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/(?P<tsworkspaceid>[0-9]+)/addindepvar/$' , views.WorkSpace.AddIndependentVar, name='AddIndependentVar'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/(?P<tsworkspaceid>[0-9]+)/setspecs/$' , views.WorkSpace.SetSpecifications, name='AddIndependentVar'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/(?P<tsworkspaceid>[0-9]+)/clear/$' , views.WorkSpace.ClearSpecification, name='ClearSpecification'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/(?P<tsworkspaceid>[0-9]+)/runestimation/$' , views.WorkSpace.RunEstimation, name='RunEstimation'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/(?P<tsworkspaceid>[0-9]+)/save/$' , views.WorkSpace.Save, name='Save'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/$' , views.ModelHomePage, name='ModelHomePage'),
    url( r'workspace/(?P<tsmodelid>[0-9]+)/new/$' , views.AddWorkSpace, name='AddWorkSpace'),
]

