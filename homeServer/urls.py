from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ServiceCategoryViewSet, ServiceViewSet, BookingViewSet, TeamViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'teams', TeamViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]

# Optional: Add a login URL for authentication if needed
urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
