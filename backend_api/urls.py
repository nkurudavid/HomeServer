from django.contrib import admin
from django.urls import include, path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homeServer.urls')),
    
    # # Optional API:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    path('api/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Configure Admin Title
admin.site.site_header = "Streamlining Home Service Solutions"
admin.site.index_title = "Management"
admin.site.site_title = "Control Panel"