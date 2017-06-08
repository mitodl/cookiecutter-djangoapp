"""
{{ cookiecutter.project_name }} views
"""
import json

from django.conf import settings
from django.shortcuts import render


def index(request):
    """
    The index view. Display available programs
    """

    host = request.get_host().split(":")[0]
    js_settings = {
        "gaTrackingID": settings.GA_TRACKING_ID,
        "host": host
    }

    return render(request, "{{ cookiecutter.project_name }}/index.html", context={
        "js_settings_json": json.dumps(js_settings),
    })
