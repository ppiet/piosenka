from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.cache import cache_control
from django.views.generic.base import View

from songs.models import Song
from artists.models import Artist


class JSONSearchIndexMixin(object):
    @cache_control(max_age=3600)
    def render_to_response(self, context):
        return self.get_json_response(json.dumps(context["index"]))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)


class ArtistSearchIndex(JSONSearchIndexMixin, View):
    def get(self, request, *args, **kwargs):
        index = []
        for artist in Artist.objects.all():
            index.append({
                "name": artist.__unicode__(),
                "value": artist.__unicode__(),
                "tokens": artist.__unicode__().split(),
                "url": artist.get_absolute_url()
            })
        return self.render_to_response({"index": index})


class SongSearchIndex(JSONSearchIndexMixin, View):
    def get(self, request, *args, **kwargs):
        index = []
        for song in Song.objects.all():
            index.append({
                "name": song.__unicode__(),
                "value": song.__unicode__(),
                "tokens": song.__unicode__().split(),
                "url": song.get_absolute_url()
            })
        return self.render_to_response({"index": index})


urlpatterns = patterns(
    '',
    url(r'^artists$', ArtistSearchIndex.as_view(), name="search_index_artists"),
    url(r'^songs$', SongSearchIndex.as_view(), name="search_index_songs"),
)
