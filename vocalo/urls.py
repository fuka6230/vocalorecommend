from django.contrib import admin
from django.urls import path, include
from .import views

app_name = 'vocalo'
urlpatterns = [
    path('result/', views.result, name='result'),
    path('tracks/', views.tracks, name='tracks'), 
    path('artists/', views.artists, name='artists'),
    path('form', views.form_name_view, name='form_name_view'),
    path('form2', views.form_artist_view, name='form_artist_view'),
    path('', views.home, name='home'),
]