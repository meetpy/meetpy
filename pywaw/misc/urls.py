from django.conf.urls import url

from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import sitemaps

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^faq/$', views.FaqView.as_view(), name='faq'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
]
