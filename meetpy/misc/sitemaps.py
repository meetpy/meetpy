from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.core.urlresolvers import reverse

from meetups.models import Meetup


class ViewSitemap(Sitemap):
    url_names = [
        'misc:home',
        'meetups:meetup_list',
        'meetups:speaker_list',
        'meetups:sponsor_list',
    ]

    def items(self):
        return self.url_names

    def location(self, item):
        return reverse(item)

sitemaps = {
    'views': ViewSitemap(),
    'meetups': GenericSitemap(info_dict={'queryset': Meetup.objects.all()}),
}