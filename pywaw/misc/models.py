import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify


def slugify_upload_to(path, fields):

    def upload_to(instance, filename):
        extension = filename.split('.')[-1]
        slug = slugify(' '.join([str(getattr(instance, field)) for field in fields]))
        new_filename = '{0}.{1}'.format(slug, extension)
        return os.path.join(path, new_filename)

    return upload_to


class Partner(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    logo = models.ImageField(upload_to=slugify_upload_to(settings.PARTNER_LOGOS_DIR, ['name']))
    is_public = models.BooleanField()

    def __str__(self):
        return self.name
