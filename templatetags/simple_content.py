from django import template

from ..models import MediaContent

register = template.Library()

@register.simple_tag
def content_media_url(slug):
    media_obj = MediaContent.objects.filter(slug=slug).first()

    if media_obj is None:
        return ''

    return media_obj.get_absolute_url()

