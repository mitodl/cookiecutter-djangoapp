"""
URLs for {{ cookiecutter.app_name }}
"""
from django.conf.urls import include, url
from {{ cookiecutter.app_name }}.views import index


urlpatterns = [
    url(r'^$', index, name='{{ cookiecutter.app_name }}-index'),
    url(r'^status/', include('server_status.urls')),
]
