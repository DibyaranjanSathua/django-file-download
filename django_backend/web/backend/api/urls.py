"""
File:           urls.py
Author:         Dibyaranjan Sathua
Created on:     19/09/20, 12:27 AM
"""
from django.urls import re_path, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import ROIView, TaskView


schema_view = get_schema_view(
    openapi.Info(
        title="ROI",
        default_version='v1',
        description="Developer: Dibyaranjan Sathua (www.sathualab.com)",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    re_path(r'^roi/$', ROIView.as_view(), name='roi'),
    path('task/<str:task_id>/', TaskView.as_view(), name='task'),
]
