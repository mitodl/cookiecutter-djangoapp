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

    js_settings = {
        "gaTrackingID": settings.GA_TRACKING_ID,
    }

    return render(request, "index.html", context={
        "js_settings_json": json.dumps(js_settings),
    })
