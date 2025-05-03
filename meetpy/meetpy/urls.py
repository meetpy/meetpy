from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path('', include(('misc.urls', 'misc'), namespace='misc')),
    path('', include(('meetups.urls', 'meetups'), namespace='meetups')),
    re_path(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
