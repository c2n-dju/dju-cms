from __future__ import print_function
from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
import django.contrib.sitemaps.views
import django.views.static
from djangocms_page_sitemap.sitemap import ExtendedSitemap
import django_cas_ng.views

from dju import views

admin.autodiscover()

p_general = [
    url(r'^sitemap\.xml$',
        django.contrib.sitemaps.views.sitemap,
        {'sitemaps': {'cmspages': ExtendedSitemap}},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    url(r'^detailed_sitemap\.xml$',
        django.contrib.sitemaps.views.sitemap,
        {'sitemaps': {'cmspages': ExtendedSitemap}, 'template_name': 'detailed_sitemap.xml'},
        name='django.contrib.sitemaps.views.detailed_sitemap'
    ),
    url(r'^robots.txt$',
        lambda r: HttpResponse("User-agent: *\nSitemap: http://www.c2n.universite-paris-saclay.fr/sitemap.xml\nDisallow: /secret_zone\n", content_type="text/plain"),
        name="robots_file"),
]

p_i18n = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    #url(r'^login/$', auth_views.login, name='login'),
    #url(r'^admin/logout/$', auth_views.logout, name='admin:logout'),
    url(r'^login/$', django_cas_ng.views.login, name='cas_login'),
    url(r'^logout/$', django_cas_ng.views.logout, name='logout'), # Il faut utiliser 'logout' pour alimenter le reverse de cms_toolbar.py
    url(r'^', include('cms.urls')),
)

p_show_media = [
    url(r'^media/(?P<path>.*)$',
        django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True},
        name='django.views.static.serve'),
]

if settings.DEBUG:
    # pour servir /media/ et /static/ dans toutes les langues
    urlpatterns = p_show_media + staticfiles_urlpatterns() + p_general + p_i18n
else:
    urlpatterns = p_general + p_i18n

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
