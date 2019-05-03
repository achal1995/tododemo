from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns =[
    path('',views.index ,name='index'),
    url(r'^about/$',views.about ,name='about'),
    url(r'^login/$',views.login ,name='login'),
    url(r'^register/$',views.register ,name='register'),
    url(r'^dashboard/$',views.dashboard ,name='dashboard'),
    url(r'^dashboard/edit$',views.edit ,name='edit'),
]