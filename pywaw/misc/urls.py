from django.conf.urls import patterns, url
from . import views
from .sitemaps import sitemaps

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^faq/$', views.FaqView.as_view(), name='faq'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
