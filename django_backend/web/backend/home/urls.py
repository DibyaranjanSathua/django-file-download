"""
File:           urls.py
Author:         Dibyaranjan Sathua
Created on:     20/09/20, 12:50 AM
"""
from django.urls import re_path
from home.views import HomeView


urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
]