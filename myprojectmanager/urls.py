from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls')),
    path('customers', include('customers.urls')),
    path('sites', include('sites.urls')),
    path('materials/', include('materials.urls')),
    path('projects/', include('projects.urls')),
    path('work_orders/', include('work_orders.urls')),
    path('bid/', include('bid.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
