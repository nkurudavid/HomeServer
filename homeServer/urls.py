from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from django.urls import path, include
from .views import UserViewSet, ServiceCategoryViewSet, ServiceViewSet, BookingViewSet, TeamViewSet

# Create the main router for top-level resources
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bookings', BookingViewSet)

# Create a nested router for 'teams' under 'bookings'
booking_router = NestedSimpleRouter(router, r'bookings', lookup='booking')
booking_router.register(r'assigned_to_team', TeamViewSet)

# Register the 'service-categories' resource with the main router
router.register(r'service-categories', ServiceCategoryViewSet)

# Create a nested router for 'service-categories' to handle 'services'
service_category_router = NestedSimpleRouter(router, r'service-categories', lookup='service_category')
service_category_router.register(r'services', ServiceViewSet)

# Define your urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(service_category_router.urls)),
    path('api/', include(booking_router.urls)),
]

# Optional: Add a login URL for authentication if needed
urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
