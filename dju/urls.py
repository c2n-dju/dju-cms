from __future__ import print_function
from cms.sitemaps import CMSSitemap
from django.conf import settings
# from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path, re_path
import django.contrib.sitemaps.views
import django.views.static
from djangocms_page_sitemap.sitemap import ExtendedSitemap
import django_cas_ng.views

from dju import views

admin.autodiscover()

p_general = [
    path('sitemap.xml',
        django.contrib.sitemaps.views.sitemap,
        {'sitemaps': {'cmspages': ExtendedSitemap}},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('detailed_sitemap.xml',
        django.contrib.sitemaps.views.sitemap,
        {'sitemaps': {'cmspages': ExtendedSitemap}, 'template_name': 'detailed_sitemap.xml'},
        name='django.contrib.sitemaps.views.detailed_sitemap'
    ),
    path('robots.txt',
        lambda r: HttpResponse("User-agent: *\nSitemap: http://www.c2n.universite-paris-saclay.fr/sitemap.xml\nDisallow: /secret_zone\n", content_type="text/plain"),
        name="robots_file"),
]

p_i18n = i18n_patterns(
    path('admin/', admin.site.urls),
    path('login/', django_cas_ng.views.LoginView.as_view(), name='cas_login'),
    path('logout/', django_cas_ng.views.LogoutView.as_view(), name='logout'), # Il faut utiliser 'logout' pour alimenter le reverse de cms_toolbar.py
    path('prototypes/', include('emencia_c2n.prototypes_urls')),
    path('', include('cms.urls')),
)

p_show_media = [
    re_path(r'^media/(?P<path>.*)$',
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
        path('__debug__/', include(debug_toolbar.urls)),
    ]
