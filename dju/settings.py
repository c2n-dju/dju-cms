# -*- coding: utf-8 -*-

import os

gettext = lambda s: s

try:
    DATA_DIR = os.environ["DJ_DATA_DIR"]
except:
    print("-- Vous avez oublié DJ_DATA_DIR le chemin static et media pour le serveur de production")
    exit(22)

try:
    DJU_DIR = os.environ["DJU_DIR"]
except:
    print("-- Vous avez oublié DJU_DIR le répertoire de .git")
    exit(22)


from dju_params.utils.git import gitsha1, gitstatus

GITSHA1 = gitsha1(DJU_DIR)
GITSTATUS = gitstatus(DJU_DIR)



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

if os.environ.get('DJ_IN_PRODUCTION', 'N') == 'Y':
    SECRET_KEY=os.environ["DJ_SECRET_KEY"]
    DEBUG=False
    ALLOWED_HOSTS = ["*"]
else:
    # Quick-start development settings - unsuitable for production
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'wqnphn7j!egz+&92$w(dt2)s#vyxrc0+xsb_i^k-hfbmsmt!h9'
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    #TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = ["*"]
    INTERNAL_IPS = ('0.0.0.0','127.0.0.1',)

if DEBUG:
    DEBUG_TOOLBAR = True
else:
    DEBUG_TOOLBAR = False

# Renforce la securite

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition

ROOT_URLCONF = 'dju.urls'

WSGI_APPLICATION = 'dju.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# chemins statiques pour le serveur de production
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static') # chemin pour collectstatic

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


SITE_ID = int(os.environ.get('SITE_ID', '1'))


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),], # vérifier : 'DIRS': [os.path.join(BASE_DIR, "dju", "templates"),],
        'APP_DIRS': True, # vérifier, définir 'loaders' impose False
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'djutags.context_processors.debug',
                'djutags.context_processors.site',
            ],
            'debug': DEBUG,
        },
    },
]

MIDDLEWARE_CLASSES = []
if DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware',]
MIDDLEWARE_CLASSES += [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', # après 'django.contrib.sessions.middleware.SessionMiddleware'
    'django.middleware.locale.LocaleMiddleware',
#    'django.middleware.doc.XViewMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware', # à la fin, appel en dernier recours
]

if os.environ.get('DJ_LOGIN_REQUIRED', 'N') == 'Y':
    MIDDLEWARE_CLASSES += ['dju.middleware.LoginRequiredMiddleware',]
    # Cf. https://docs.djangoproject.com/fr/1.11/topics/auth/customizing/
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'dju.backends.DjuCASBackend',
    ]

    CAS_SERVER_URL = os.environ['CAS_SERVER_URL']
    CAS_ADMIN_PREFIX = 'admin'
    LOGIN_URL = '/login/'
    CAS_LOGOUT_COMPLETELY = True
    CAS_VERSION = 'CAS_2_SAML_1_0'
    CAS_APPLY_ATTRIBUTES_TO_USER = False
    CAS_CREATE_USER = True # A better way to give access to unregistred lab members have to be found 
    C2N_SAML_CONTROL = (os.environ['DJU_SAML_CONTROL_KEY'], os.environ['DJU_SAML_CONTROL_VALUE'])
elif os.environ.get('DJ_IN_PRODUCTION', 'Y') == 'N':
    AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
else:
    AUTHENTICATION_BACKENDS = []
    
    
# Les applications prioritaires doivent venir en premier dans INSTALLED_APPS (la première définition a priorité)
# Cf. https://docs.djangoproject.com/fr/1.11/ref/settings/#s-installed-apps

INSTALLED_APPS = (
    ### Entries for applications with plugins should come after cms ###
    'cms',
    ### core addons ###
    ### Cf. https://www.django-cms.org/en/blog/2017/02/01/core-addons/
    'filer',
    'djangocms_admin_style', # add before 'django.contrib.admin'
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_file',
    'djangocms_snippet', # potential security risk /!\
    'djangocms_style',
    'djangocms_video',
    ### deprecated applications ###
    ### migrer les pages avant suppressions Cf. https://www.django-cms.org/en/blog/2017/02/01/core-addons/
    #'cmsplugin_filer_file',
    #'cmsplugin_filer_folder',
    #'cmsplugin_filer_link',
    #'cmsplugin_filer_image',
    #'cmsplugin_filer_teaser',
    #'cmsplugin_filer_video',
    ### pour le sitemap ###
    'djangocms_page_sitemap',
    ### pour améliorer djangocms_text_ckeditor ###
    # 'softhyphen',
    ### django ###
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    ### applications complémentaires django ###
    'easy_thumbnails',
    'treebeard',
    'menus',
    'sekizai',
    'django_extensions',
    'django_cas_ng',
    ### DJU Apps ###
    'dju',
    'djutags',
    'dju_cmstags',
    'dju_page_thumbnail',
    'dju_menuzen',
    'dju_sites',
    'dju_params',
)

### Private Apps ###
if os.environ.get('USE_PRIVATE_STUFF', 'Y') == 'Y':
    INSTALLED_APPS += (
        'dju_semin.core',
        'dju_semin.cms',
        'dju_actu.core',
        'dju_actu.cms',
    )

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ('debug_toolbar',)


LOCALE_PATHS = [
        DJU_DIR + "/locale",
    ]
    
LANGUAGES = (
    ('fr', gettext('fr')),
    ('en', gettext('en')),
)

CMS_LANGUAGES = {
    'default': {
        'fallbacks': ['en', 'fr'],
        'public': True,
        'hide_untranslated': True,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'fr',
            'hide_untranslated': False,
            'name': gettext('fr'),
            'redirect_on_fallback': True,
        },
        {
            'public': True,
            'code': 'en',
            'hide_untranslated': False,
            'name': gettext('en'),
            'redirect_on_fallback': True,
        },
    ],
}

CMS_TEMPLATES = (
    ('snipA.html', 'Snippets A'),
    ('snipB.html', 'Snippets B'),
    ('snipC.html', 'Snippets C'),
    ('snipD.html', 'Snippets D'),
    ('snipZ.html', 'Snippets Z'),
)

if os.environ.get('USE_PRIVATE_STUFF', 'Y') == 'Y':
    CMS_TEMPLATES += (
        ('F_C2N_page_left-nav_10.html', 'F5 Nav(2) Content(10)'),
        ('F_C2N_page_left-navigation_9.html', 'F5 Nav(3) Content(9)'),
        ('F_C2N_12.html', 'F5 Content(12)'),
        ('f6/content_12.html', 'F6 Content(12)'),
        ('f6.4/content_12.html', 'F6.4 Content(12)'),
        ('F_C2N_4_8.html', 'F5 Info(4) Content(8)'),
        ('f6/info2_4-content_8.html', 'F6 Info(4) Content(8)'),
        ('F_C2N_departement.html', 'F5-Departement'),
        ('f6/equipe-content_12.html', 'F6-Equipe Content(12)'),
        ('f6/departement.html', 'F6-Departement'),
        ('F_C2N_formation.html', 'F5-Formation'),
        ('F_C2N_plateforme.html', 'F5-Plateforme'),
        #
        ('utils/migrateur.html', 'Migrateur de placeholders'),
        #
        ('F_C2N_staff_ressources.html', 'F5-Staff-Ressources'),
        #
        ('f6/actu_8-semin_4.html', 'F6 Actu(8) Semin(4)'),
        #
    )

CMS_PERMISSION = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

try:
    base = os.environ['DJBASE']
except KeyError:
    print("-- Vous avez oublié : export DJBASE=base_XXXXX_XX") 
    exit(22)
try:
    intrabase = os.environ['INTRABASE']
except KeyError:
    print("-- Vous avez oublié : export INTRABASE=base_XXXXX_XX") 
    exit(22)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': base,
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    },
    'dbcore': { # ex dbsemin, dbdata
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': intrabase,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

DATABASE_ROUTERS = ["dju.routers.DataRouter", ]

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

FILER_DEBUG = True
FILER_IMAGE_USE_ICON = True
#TEXT_SAVE_IMAGE_FUNCTION='cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'
TEXT_ADDITIONAL_TAGS = ('iframe',)
TEXT_ADDITIONAL_ATTRIBUTES = ('scrolling', 'allowfullscreen', 'frameborder', 'src', 'height', 'width')

CMSPLUGIN_FILER_IMAGE_STYLE_CHOICES = (
    ('default', 'Default'),
    ('circle', 'Circle'),
)
CMSPLUGIN_FILER_IMAGE_DEFAULT_STYLE = 'Default'

CKEDITOR_SETTINGS = {
    # Cf. http://docs.ckeditor.com/#!/guide/dev_output_format
    'dataIndentationChars': '  ',
    #
    'fontSize_sizes': 'smaller;larger;xx-small;x-small;small;large;x-large;xx-large',
    'stylesSet': [
        { 'name': 'strong (important)', 'element': 'strong' },
        { 'name': 'b (gras)', 'element': 'b' },
        { 'name': 'em (en évidence)', 'element': 'em' },
        { 'name': 'dfn (définition)', 'element': 'dfn' },
        { 'name': 'i (italique)', 'element': 'i' },
        { 'name': 'small (petit)', 'element': 'small' },
        { 'name': 'sub (indice)', 'element': 'sub' },
        { 'name': 'sup (exposant)', 'element': 'sup' },
        { 'name': 'code (informatique)', 'element': 'code' },
        { 'name': 'samp (résultat informatique)', 'element': 'samp' },
        { 'name': 'kbd (clavier)', 'element': 'kbd' },
        { 'name': 'var (variable informatique)', 'element': 'var' },
        { 'name': 'mark (marqué)', 'element': 'mark' },
        { 'name': 's (incorrect)', 'element': 's' },
        { 'name': 'del (effacé)', 'element': 'del' },
        { 'name': 'ins (inséré)', 'element': 'ins' },
        { 'name': 'cite (titre d\'article)', 'element': 'cite' },
        { 'name': 'quot (courte citation)', 'element': 'q' },
        { 'name': 'u (souligné à éviter)', 'element': 'u' },
        { 'name': 'span (style à remplir)', 'element': 'span' },
        ],
    'removeFormatTags': 'b,cite,code,del,dfn,em,i,ins,kbd,marker,q,s,samp,small,span,strong,sub,sup,u,var', # obsolète : big,font,strike,tt
    'format_tags': 'p;h1;h2;h3;h4;h5;h6;div;pre',
    'font_names':'Arial/Arial, Helvetica, sans-serif; Times New Roman/Times New Roman, Times, serif; Verdana;',
    'language': '{{ language }}',
    'toolbar_CMS': [
        [ 'cmsplugins', ],
        [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ],
        ['Format'], [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', '-', 'Blockquote', 'CreateDiv'], ['HorizontalRule', 'PageBreak'], #'NewPage'
        ['RemoveFormat', 'Styles',  'Bold', 'Italic', '-', 'Subscript', 'Superscript', '-', 'TextColor', 'BGColor', '-', 'Smiley', 'SpecialChar', 'Font', 'FontSize', 'RemoveFormat'],
        # rare et dans stylesSet  'Underline', 'Strike',
        [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt'],
        [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField', 'Link', 'Unlink', 'Anchor', 'Image', 'Flash', 'Table', 'Iframe', 'Preview', 'Print', 'About',],
        # ?? ['Templates'],
        #[ 'c2nicon','c2nlinkpeople','c2nwidget'],
        ['ShowBlocks', 'Source'],
        # semble inutile ['Maximize'],
    ],
    'skin': 'moono',
    #'colorButton_colors': 'B22222,FFFFFF',
    #'extraPlugins': 'c2nicon,c2nlinkpeople,lineutils,clipboard,widget,c2nwidget',
}

# Il faut donner dans cette construction des menu de plugins les noms de classe : grep -r CMSPluginBase .. | grep class

CMS_PLACEHOLDER_CONF = {
    None: {
        # On ne met rien donc on montre tout !
        #"plugins": ['TextPlugin'],
	'excluded_plugins': ['InheritPlugin', 'FilerFilePlugin', 'FilerFolderPlugin',
                             'FilerImagePlugin', 'FilerLinkPlugin', 'FilerTeaserPlugin', 'FilerVideoPlugin',],
    },
    'content': {
        'plugins': ['StylePlugin', 'TextPlugin', 'LinkPlugin', 'PicturePlugin', 'FilePlugin',
                    'VideoPlayerPlugin', 'FolderPlugin', 'ActuPluginPublisher', 'SeminPluginPublisher',],
        #'extra_context': {"width":640},
        'name': gettext("Content"),
        'language_fallback': True,
        #'default_plugins': [
        #    {
        #        'plugin_type': 'TextPlugin',
        #        'values': {
        #            'body':'<p>Lorem ipsum dolor sit amet...</p>',
        #        },
        #    },
        #],
        'child_classes': {
            'TextPlugin': ['PicturePlugin', 'LinkPlugin', 'FilePlugin', 'FolderPlugin', 'StylePlugin', 'SnippetPlugin'], # 'VideoSourcePlugin', 'VideoTrackPlugin',
        },
        #'parent_classes': {
        #    'LinkPlugin': ['TextPlugin'],
        #},
    },
}


MIGRATION_MODULES = {
}


CMSPLUGIN_CASCADE_PLUGINS = ('cmsplugin_cascade.bootstrap3',)
CMSPLUGIN_CASCADE_PLUGINS += ('cmsplugin_cascade.link',)


CMSPLUGIN_CASCADE_ALIEN_PLUGINS = ('TextPlugin', 'FilerImagePlugin',)

CMSPLUGIN_FILER_IMAGE_STYLE_CHOICES = (
    ('default', 'Default'),
    ('circle', 'Circle'),


)
CMSPLUGIN_FILER_IMAGE_DEFAULT_STYLE = 'Default'
FILER_DUMP_PAYLOAD = True

DJANGOCMS_SNIPPET_CACHE = False

# PAGE_SITEMAP_DEFAULT_CHANGEFREQ="daily"
# PAGE_SITEMAP_CACHE_DURATION=0

try:
    isHttps = os.environ['DJ_HTTPS']
except KeyError:
    print("-- Vous avez oublié : export DJHTTPS=true/false") 
    exit(22)

if isHttps == "Y":
    # print 'DJ_HTTPS = ' + isHttps
    # dangereux et pas utile : SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

