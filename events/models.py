from datetime import datetime
from datetime import timedelta
import uuid

from django.core.exceptions import ValidationError
from django.db import models

from artists.models import Entity
from content.trevor import render_trevor, put_text_in_trevor
from content.models import ContentItem
from content.slug import SlugMixin


class Venue(SlugMixin, models.Model):
    name = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    slug = models.SlugField(max_length=100, unique=True, editable=False)
    lat = models.FloatField(null=True, editable=False, help_text="Latitude.")
    lon = models.FloatField(null=True, editable=False, help_text="Longtitude.")

    @staticmethod
    def create_for_testing():
        venue = Venue()
        venue.name = str(uuid.uuid4()).replace("-", "")
        venue.town = "New York"
        venue.street = "233 Madison Avenue"
        venue.lat = 0.0
        venue.lon = 0.0
        venue.save()
        return venue

    class Meta:
        ordering = ["town", "name"]

    def __str__(self):
        return "%s - %s" % (self.town, self.name)

    def clean(self):
        super().clean()
        from pygeocoder import Geocoder
        from pygeolib import GeocoderError
        address = str(self.street) + ', ' + str(self.town)
        try:
            geo = Geocoder.geocode(address)
            self.lat, self.lon = geo[0].coordinates
        except GeocoderError:
            # Geo lookup failed to recognize this address.
            pass

    @models.permalink
    def get_absolute_url(self):
        return('venue_detail', (), {
            'slug': self.slug,
        })

    # SlugMixin:
    def get_slug_elements(self):
        assert self.name
        assert self.town
        return [self.name, self.town]


class Event(SlugMixin, ContentItem):
    HELP_NAME = """Nazwa wydarzenia, np. 'Koncert pieśni Jacka Kaczmarskiego'
lub 'V Festiwal Piosenki Wymyślnej w Katowicach'."""
    HELP_PRICE = """E.g. 20zł, wstęp wolny. W przypadku braku danych pozostaw
puste."""
    HELP_WEBSITE = """Strona internetowa wydarzenia, źródło informacji. W
przypadku braku danych pozostaw puste."""

    name = models.CharField(max_length=100, help_text=HELP_NAME)
    datetime = models.DateTimeField()
    venue = models.ForeignKey(Venue)
    description_trevor = models.TextField()
    price = models.CharField(max_length=100, null=True, blank=True,
                             help_text=HELP_PRICE)
    website = models.URLField(null=True, blank=True,
                              help_text=HELP_WEBSITE)

    slug = models.SlugField(max_length=100, unique_for_date="datetime",
                            editable=False)
    description_html = models.TextField(editable=False)

    @staticmethod
    def create_for_testing(author, venue=None):
        event = Event()
        event.author = author
        event.name = str(uuid.uuid4()).replace("-", "")
        event.description_trevor = put_text_in_trevor("Abc")
        event.datetime = datetime.now() + timedelta(days=365)
        event.venue = venue if venue else Venue.create_for_testing()
        event.save()
        return event

    class Meta(ContentItem.Meta):
        ordering = ["datetime"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = render_trevor(self.description_trevor)
        super().save(*args, **kwargs)

    def get_url_params(self):
        return {
            'year': self.datetime.strftime("%Y"),
            'month': self.datetime.strftime("%m"),
            'day': self.datetime.strftime("%d"),
            'slug': self.slug
        }

    @models.permalink
    def get_absolute_url(self):
        return ('event_detail', (), self.get_url_params())

    @models.permalink
    def get_edit_url(self):
        return ('edit_event', (), self.get_url_params())

    @models.permalink
    def get_review_url(self):
        return ('review_event', (), self.get_url_params())

    @models.permalink
    def get_approve_url(self):
        return ('approve_event', (), self.get_url_params())

    # SlugMixin:
    def get_slug_elements(self):
        assert self.name
        assert self.venue and self.venue.town
        return [self.name, self.venue.town]

    def lat(self):
        return self.venue.lat

    def lon(self):
        return self.venue.lon

    def performers(self):
        return [x.entity for x in EntityPerformance.objects.filter(event=self)]


class EntityPerformance(models.Model):
    event = models.ForeignKey(Event)
    entity = models.ForeignKey(Entity)

    class Meta:
        unique_together = ("event", "entity")

    def clean(self):
        super().clean()
        if not self.entity.still_plays:
            raise ValidationError("Ten artysta nie koncertuje.")
