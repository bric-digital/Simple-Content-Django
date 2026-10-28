from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render, redirect

from .models import PageContent, MediaContent

def simple_content_page(request, slug):
    context = {
        'page': get_object_or_404(PageContent, slug=slug)
    }

    return render(request, 'simple_content_page.html', context=context)

def simple_content_media(request, slug):
    media_obj = get_object_or_404(MediaContent, slug=slug)

    if media_obj.content_url is not None:
        return redirect(media_obj.content_url)

    file_handle = media_obj.content_file.open()

    return HttpResponse(file_handle, content_type=media_obj.content_type)
