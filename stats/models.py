from django.db import models
import uuid
from hashlib import sha1
import hmac
from django.template.defaultfilters import slugify
from datetime import datetime


class Project(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=100)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        self.slug = slugify(self.name)
        return super(Project, self).save(*args, **kwargs)

    def generate_key(self):
        #shamelessly lifted from django-tastypie ApiKey
        # Get a random UUID.
        new_uuid = uuid.uuid4()
        # Hmac that beast.
        return hmac.new(str(new_uuid), digestmod=sha1).hexdigest()


class Metric(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:50]
        return super(Metric, self).save(*args, **kwargs)


class MetricData(models.Model):
    metric = models.ForeignKey(Metric)
    value = models.FloatField()
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        super(MetricData, self).save(*args, **kwargs)


class Instrument(models.Model):
    metric = models.ForeignKey(Metric)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    annotations = models.TextField(default="[]")
    aggregations = models.TextField(default="[]")
    values = models.TextField(default="[]")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:50]
        return super(Instrument, self).save(*args, **kwargs)


class Event(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=255)
    description = models.TextField()
