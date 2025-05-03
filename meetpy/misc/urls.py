from django.urls import path, re_path
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import sitemaps

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
]
