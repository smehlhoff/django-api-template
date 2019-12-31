from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework import status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('backend.users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER')
admin.site.index_title = getattr(settings, 'ADMIN_SITE_INDEX_TITLE')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE')
admin.site.site_url = getattr(settings, 'SITE_URL')


def page_not_found(request, *args, **kwargs):
    response = {
        'error': {
            'message': 'Page not found.'
        }
    }

    return JsonResponse(response, status=status.HTTP_404_NOT_FOUND)


def server_error(request, *args, **kwargs):
    response = {
        'error': {
            'message': 'The server encountered an internal error.'
        }
    }

    return JsonResponse(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


handler404 = page_not_found
handler500 = server_error
