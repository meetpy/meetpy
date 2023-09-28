from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import set_language

admin.autodiscover()

urlpatterns = [
    url(r'^', include(('misc.urls', 'misc'), namespace='misc')),
    url(r'^', include(('meetups.urls', 'meetups'), namespace='meetups')),
    url(r'^set_language/$', set_language, name='set_language'),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
