"""
File:           tasks.py
Author:         Dibyaranjan Sathua
Created on:     19/09/20, 6:55 PM
"""
import time
import os
import glob
import re
import datetime

import pandas as pd
from celery import shared_task
from django.conf import settings


@shared_task
def download_roi_file(cities, max_price, property_type, foreclose, renovation):
    """ Download ROI CSV file for all the cities """
    results = dict()
    cities_list = [x.strip() for x in cities.split(',')]
    csvfiles = glob.glob(os.path.join(settings.CSV_ROOT, '*'))
    regex = re.compile(r'output_(.*?)_.*\.csv')
    cities_available = dict()
    for file in csvfiles:
        match_str = regex.search(file)
        if match_str:
            city_name = match_str.group(1)
            cities_available[city_name.lower()] = file

    frames = []
    for city in cities_list:
        if city.lower() in cities_available.keys():
            frames.append(pd.read_csv(cities_available[city.lower()]))
        else:
            results['error'] = f'{city} is not present in database. ' \
                               f'Remove {city} from the list and try again.'
            return results

    df = pd.concat(frames)
    df = df[df['purchase_price'] <= int(max_price)]
    df = df[df['foreclosure'] == foreclose]
    current_date_str = datetime.date.today().strftime('%Y_%m_%d')
    output_filename = f'{"_".join(cities_list)}_{current_date_str}.csv'
    output_filepath = os.path.join(settings.ROI_ROOT, output_filename)
    df.to_csv(output_filepath)
    results['error'] = ''
    results['filename'] = output_filename
    results['filepath'] = f'{settings.ROI_URL}/{output_filename}'
    time.sleep(2)
    return results
