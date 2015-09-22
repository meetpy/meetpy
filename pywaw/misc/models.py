import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.deconstruct import deconstructible


@deconstructible
class SlugifyUploadTo(object):

    def __init__(self, path, fields):
        self.path = path
        self.fields = fields

    def __call__(self, instance, filename):
        extension = filename.split('.')[-1]
        slug = slugify(' '.join([str(getattr(instance, field)) for field in self.fields]))
        new_filename = '{0}.{1}'.format(slug, extension)
        return os.path.join(self.path, new_filename)


class Partner(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    logo = models.ImageField(upload_to=SlugifyUploadTo(settings.PARTNER_LOGOS_DIR, ['name']))
    is_public = models.BooleanField()

    def __str__(self):
        return self.name
