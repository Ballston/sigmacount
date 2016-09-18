from django.conf.urls import url

from . import views

urlpatterns = [
    url( r'^$', views.Load, name='LoadData'),
    url( r'(?P<dataset_id>\d+)' , views.ExploreData, name='ExploreData'),
    #url(r'mygraph/(?P<pk>\d+)\.png', views.graphic, name='mygraph'),
    #url(r'mygraph/hiddengraphic.png', views.hiddengraphic.hiddengraphic , name='hiddengraphic'),
]

