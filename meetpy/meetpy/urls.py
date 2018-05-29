from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^', include('misc.urls', namespace='misc')),
    url(r'^', include('meetups.urls', namespace='meetups')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
