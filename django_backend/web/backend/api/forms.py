"""
File:           forms.py
Author:         Dibyaranjan Sathua
Created on:     19/09/20, 9:08 PM
"""
from django import forms


class ROIForm(forms.Form):
    """ Form to upload data to download ROI data """
    cities = forms.CharField(required=True)

