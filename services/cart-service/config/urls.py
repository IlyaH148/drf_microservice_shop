from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'cart-service'})

urlpatterns = [
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('api/', include('apps.cart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

