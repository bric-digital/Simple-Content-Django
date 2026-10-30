# pylint: disable=line-too-long

import json

from django.conf import settings
from django.contrib import admin

try:
    from docker_utils.admin import PortableModelAdmin as ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin as ModelAdmin # pylint: disable=useless-import-alias

from .models import PageCollection, PageContent, MediaContent

@admin.register(PageCollection)
class PageCollectionAdmin(ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title', 'slug', 'content', 'content_rendered', 'search_content', 'notes',)

@admin.register(PageContent)
class PageContentAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'is_template',)
    search_fields = ('title', 'slug', 'content', 'content_rendered', 'search_content', 'notes',)
    list_filter = ('is_template', 'belongs_to')


@admin.register(MediaContent)
class MediaContentAdmin(ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title', 'slug', 'description', 'description_rendered', 'search_content', 'notes',)
    list_filter = ('belongs_to',)
