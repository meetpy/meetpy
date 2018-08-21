from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^', include(('misc.urls', 'misc'), namespace='misc')),
    url(r'^', include(('meetups.urls', 'meetups'), namespace='meetups')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
