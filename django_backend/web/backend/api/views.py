from pathlib import Path

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.conf import settings

from celery import current_app

from .tasks import download_roi_file


class ROIView(View):
    """ Download ROI file """

    def get(self, request):
        """ Return CSV file using user query inputs """
        cities = request.GET.get('cities')
        max_price = request.GET.get('max_price')
        property_type = request.GET.get('property_type', 'flat')
        foreclose = request.GET.get('foreclose', 'false') == 'true'
        renovation = request.GET.get('renovation', 'false') == 'true'
        task = download_roi_file.delay(cities, max_price, property_type, foreclose, renovation)
        context = dict()
        context['task_id'] = task.id
        context['task_status'] = task.status
        return render(request, 'api/download.html', context)
        #response_data = {'task_status': task.status, 'task_id': task.id}
        #return JsonResponse(response_data)
        # response = HttpResponse()
        # file_path = Path(settings.ROI_ROOT) / 'output_Rostock_2020_Sep_11_19_48.csv'
        # with open(file_path, 'r') as infile:
        #     response = HttpResponse(infile.read(), content_type="application/text")
        #     response['Content-Disposition'] = 'attachment; filename=output_roi.csv'
        #     return response


class TaskView(View):
    """ Download file """

    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)
