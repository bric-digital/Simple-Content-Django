# pylint: disable=line-too-long, no-member

import json

from django.contrib import messages
from django.core import serializers

from .models import PageCollection, PageContent, MediaContent

def import_objects(file_type, import_file):
    if file_type == 'simple_content.pagecollection':
        return import_page_collections(import_file)

    if file_type == 'simple_content.pagecontent':
        return import_page_contents(import_file)

    if file_type == 'simple_content.mediacontent':
        return import_media_contents(import_file)

    return None

def import_page_collections(import_file):
    user_messages = []

    with import_file.open() as file_stream:
        collections_json = json.load(file_stream)

        collections_imported = 0

        for collection_json in collections_json:
            if collection_json.get('model', None) == 'simple_content.pagecollection':
                collection_obj = PageCollection()

                for field_key in collection_obj.get('fields', {}).keys():
                    field_value = collection_obj.get('fields', {}).get(field_key, None)

                    setattr(collection_obj, field_key, field_value)

                collection_obj.save()

                collections_imported += 1

        if collections_imported > 1:
            user_messages.append(('%s page collections imported.' % collections_imported, messages.SUCCESS))
        elif collections_imported == 1:
            user_messages.append(('1 page collection imported.', messages.SUCCESS))
        else:
            user_messages.append(('No page collections imported.', messages.INFO))

    return user_messages

def import_page_contents(import_file):
    user_messages = []

    templates = {}

    pages_imported = 0

    with import_file.open() as file_stream:
        pages_json = json.load(file_stream)

        pages_imported = 0

        for page_json in pages_json: # pylint: disable=too-many-nested-blocks
            if page_json.get('model', None) == 'simple_content.pagecontent':
                page_obj = PageContent()

                for field_key in page_json.get('fields', {}).keys():
                    field_value = page_json.get('fields', {}).get(field_key, None)

                    if field_key in ('template_page',):
                        if field_value is not None:
                            # Wire up to template ONLY after the templates actually exist.

                            slug_list = templates.get(field_value, [])

                            slug_list.append(slug_list)

                            templates[field_value] = slug_list

                            field_value = None

                    setattr(page_obj, field_key, field_value)

                page_obj.save()

                pages_imported += 1

        for page_slug, page_template in templates:
            template_page = PageContent.objects.filter(slug=page_slug).first()

            if template_page is not None:
                for child_page in page_template:
                    child_page.template_page = template_page
                    child_page.save()

        if pages_imported > 1:
            user_messages.append(('%s pages imported.' % pages_json, messages.SUCCESS))
        elif pages_imported == 1:
            user_messages.append(('1 pages imported.', messages.SUCCESS))
        else:
            user_messages.append(('No pages imported.', messages.INFO))

    return user_messages

def import_media_contents(import_file):
    user_messages = []

    with import_file.open() as file_stream:
        medias_json = json.load(file_stream)

        medias_imported = 0

        for media_json in medias_json: # pylint: disable=too-many-nested-blocks
            if media_json.get('model', None) == 'simple_content.mediacontent':
                media_obj = MediaContent()

                file_content = None

                for field_key in media_json.get('fields', {}).keys():
                    field_value = media_json.get('fields', {}).get(field_key, None)

                    if field_key in ('content_file',):
                        pass # Load in image to file_content.
                    else:
                        setattr(media_obj, field_key, field_value)

                media_obj.save()

                if file_content is not None:
                    pass # Save file to object

                pages_imported += 1

        if medias_imported > 1:
            user_messages.append(('%s media content objects imported.' % medias_json, messages.SUCCESS))
        elif medias_imported == 1:
            user_messages.append(('1 media content object imported.', messages.SUCCESS))
        else:
            user_messages.append(('No media content objects imported.', messages.INFO))

    return user_messages

def export_page_collections(queryset):
    to_export = []

    for page_collection in queryset:
        page_collection_json = json.loads(serializers.serialize('json', PageCollection.objects.filter(pk=page_collection.pk)))[0]

        del page_collection_json['pk']

        to_export.append(page_collection_json)

    return to_export

def export_page_contents(queryset):
    to_export = []

    for page_content in queryset:
        django_object = PageContent.objects.filter(pk=page_content.pk)

        page_content_json = json.loads(serializers.serialize('json', django_object))[0]

        del page_content_json['pk']

        if page_content_json.template_page is not None:
            page_content_json['fields']['template_page'] = django_object.template_page.slug

        belongs_to = []

        for page_collection in django_object.belongs_to.all():
            belongs_to.append(page_collection.slug)

        page_content_json['belongs_to'] = belongs_to

        to_export.append(page_content_json)

    return to_export

def export_media_contents(queryset):
    to_export = []

    for media_content in queryset:
        django_object = MediaContent.objects.filter(pk=media_content.pk)

        media_content_json = json.loads(serializers.serialize('json', django_object))[0]

        del media_content_json['pk']

        # Capture file content and local filename and serialize as Base64

        belongs_to = []

        for page_collection in django_object.belongs_to.all():
            belongs_to.append(page_collection.slug)

        media_content_json['belongs_to'] = belongs_to

        to_export.append(media_content_json)

    return to_export

def export_objects(queryset, queryset_name):
    to_export = []

    if queryset_name == 'PageCollection':
        to_export.extend(export_page_collections(queryset))
    elif queryset_name == 'PageContent':
        to_export.extend(export_page_contents(queryset))
    elif queryset_name == 'MediaContent':
        to_export.extend(export_media_contents(queryset))

    return to_export
