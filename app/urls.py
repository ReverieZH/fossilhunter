from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from app import views

urlpatterns = [
    url(r'^getspeciesguide', views.Getspeciesguide.as_view()),
    url(r'^setsearch', views.Setsearch.as_view()),
    url(r'^getspeciesdetail/(?P<pk>\d+)/$', views.Getspeciesdetail.as_view()),
    url(r'^getmyfossil/', views.Getmyfossil.as_view()),
    url(r'^setdocumentchange/', views.Setdocumentchange.as_view()),
    url(r'^setphoto', views.SetPhoto.as_view()),
    url(r'^setresult', views.Setresult.as_view()),
    url(r'^getresult', views.Getresult.as_view()),
    url(r'^getreconstruct', views.Getreconstruct.as_view()),
    url(r'^getnews', views.Getnews.as_view()),

    url(r'^getuser/', views.GetUserDetail.as_view()),
    url(r'^user/(?P<pk>\d+)/$', views.User.as_view()),
    url(r'^geteveryfossil', views.GetFossilFamily.as_view()),
    url(r'^getmycollection/', views.GetMyCollection.as_view()),
    url(r'^setcollection/', views.SetCollection.as_view()),
    url(r'^deletepicture/', views.Deletepicture.as_view()),

    url(r'^getstudyAdverstation/', views.GetstudyAdverstation.as_view()),
    url(r'^getAdverstation/', views.GetAdverstation.as_view()),
    url(r'^getNewsReport/', views.GetNewsReport.as_view()),
    url(r'^EveryonePublish/', views.EveryonePublish.as_view()),
    url(r'^OnePublish/(?P<pk>\d+)/$', views.OnePublish.as_view()),
    url(r'^UserPublish/(?P<pk>\d+)/$', views.UserPublish.as_view()),
    url(r'^Comment/$', views.Comment.as_view()),
    url(r'^map/$', views.MapView),
]
