# pylint: disable=line-too-long, wrong-import-position

import sys

if sys.version_info[0] > 2:
    from django.urls import re_path as url # pylint: disable=no-name-in-module
else:
    from django.conf.urls import url

from .views import simple_content_page, simple_content_media

urlpatterns = [
    url(r'^p/(?P<slug>.+)$', simple_content_page, name='simple_content_page'),
    url(r'^m/(?P<slug>.+)$', simple_content_media, name='simple_content_media'),
]

