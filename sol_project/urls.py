from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace.urls')),
]

# Serve media files in development (DEBUG=True)
# In production, media files should ideally be served from cloud storage.
# For small-scale use, the below also enables serving on production.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
