# pylint: disable=line-too-long, no-member

import mimetypes

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.template.loader import render_to_string
from django.template import Template, Context
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

class PageCollection(models.Model):
    title = models.CharField(max_length=8192)
    slug = models.SlugField(max_length=1024, unique=True)
    content = MarkdownField(rendered_field='content_rendered', validator=VALIDATOR_STANDARD, null=True, blank=True)
    content_rendered = RenderedMarkdownField()
    search_content = models.TextField(max_length=(1024 * 1024), blank=True)

    notes = models.TextField(max_length=(1024 * 1024), null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.slug)

class PageContent(models.Model):
    title = models.CharField(max_length=8192)
    slug = models.SlugField(max_length=1024, unique=True)
    content = MarkdownField(rendered_field='content_rendered', validator=VALIDATOR_STANDARD, null=True, blank=True)
    content_rendered = RenderedMarkdownField()
    search_content = models.TextField(max_length=(1024 * 1024), null=True, blank=True)

    head_content = models.TextField(max_length=(1024 * 1024), null=True, blank=True)

    is_template = models.BooleanField(default=False)

    template_page = models.ForeignKey('PageContent', related_name='uses', on_delete=models.SET_NULL, null=True, blank=True)

    notes = models.TextField(max_length=(1024 * 1024), null=True, blank=True)

    belongs_to = models.ManyToManyField(PageCollection, related_name='member_pages', blank=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.slug)

    def get_absolute_url(self):
        return reverse('simple_content_page', args=[self.slug])

    def render(self):
        context = {
            'page': self
        }

        if self.template_page is not None:
            template = Template('{% load simple_content %}' + self.template_page.content_rendered)

            return template.render(Context(context))

        template = Template('{% load simple_content %}' + self.content_rendered)

        return template.render(Context(context))

    def get_head(self):
        context = {
            'page': self,
        }

        template = Template('{% load simple_content %}' + self.head_content)

        return template.render(Context(context))

class MediaContent(models.Model):
    title = models.CharField(max_length=8192)
    slug = models.SlugField(max_length=1024, unique=True)
    content_type = models.CharField(max_length=256, null=True, blank=True)

    description = MarkdownField(rendered_field='description_rendered', validator=VALIDATOR_STANDARD, null=True, blank=True)
    description_rendered = RenderedMarkdownField()
    search_content = models.TextField(max_length=(1024 * 1024), null=True, blank=True)

    content_file = models.FileField(null=True, blank=True, upload_to='simple_content_media')
    content_url = models.URLField(null=True, blank=True)

    belongs_to = models.ManyToManyField(PageCollection, related_name='member_media', blank=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.slug)

    def get_absolute_url(self):
        return reverse('simple_content_media', args=[self.slug])

@receiver(post_save, sender=MediaContent)
def set_content_type(sender, instance, **kwargs):
    if instance.content_type is None and (instance.content_file in ('', None,)) is False:
        (content_type, encoding) = mimetypes.guess_type(instance.content_file.path)

        if content_type is not None:
            instance.content_type = content_type
            instance.save()
