from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('account.urls', 'app_name'), namespace='account')),
    path('', include(('store.urls', 'app_name'), namespace='store')),
    path('order/', include(('order.urls', 'app_name'), namespace='order')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
