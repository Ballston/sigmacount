from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.loginview, name='loginview'),
    url(r'^logout/', views.logoutview, name='logoutview'),
    url(r'^$',views.homepage,name='homepage'),
    url(r'createproject/(?P<projecttype>\w+)', views.createproject, name='createproject'),
    #url(r'mygraph/(?P<pk>\d+)\.png', views.graphic, name='mygraph'),
    #url(r'mygraph/hiddengraphic.png', views.hiddengraphic.hiddengraphic , name='hiddengraphic'),
]