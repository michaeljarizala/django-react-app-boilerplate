from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.sites.AdminSite.site_header = 'Django-React App Boilerplate Admin Portal'
admin.sites.AdminSite.site_title = 'Django-React App Boilerplate  Admin Portal'
admin.sites.AdminSite.index_title = 'Django-React App Boilerplate Admin Portal'

urlpatterns = [
    re_path(r'^summernote/', include('django_summernote.urls')),

    path('admin/', admin.site.urls),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns