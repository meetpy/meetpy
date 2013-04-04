from django.conf.urls import patterns, url
from misc import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view()),
)
