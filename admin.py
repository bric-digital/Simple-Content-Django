# pylint: disable=line-too-long

import json

from django.conf import settings
from django.contrib import admin

from .models import PageCollection, PageContent, MediaContent

@admin.register(PageCollection)
class PageCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title', 'slug', 'content', 'content_rendered', 'search_content', 'notes',)

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_template',)
    search_fields = ('title', 'slug', 'content', 'content_rendered', 'search_content', 'notes',)
    list_filter = ('is_template', 'belongs_to')


@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title', 'slug', 'description', 'description_rendered', 'search_content', 'notes',)
    list_filter = ('belongs_to',)
