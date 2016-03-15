"""
URLs for {{ cookiecutter.app_name }}
"""
from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='{{ cookiecutter.app_name }}/index.html'),
        name='{{ cookiecutter.app_name }}-index'
    ),
    url(r'^status/', include('server_status.urls')),
]
