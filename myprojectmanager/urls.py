from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls')),
    # path('work_orders/', include('work_orders.urls')),
    path('admin/', admin.site.urls),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
