from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views.address_views import AddressViewSet
from user.views.user_views import CreateTokenView, CreateUserView, ManageUserView
# from user.views.role_views import RoleListCreateView, RoleDetailView  # Import role views

app_name = 'user'

# Create a router and register our viewsets
router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')

# Register role-related views with the router
# role_router = DefaultRouter()
# role_router.register('roles', RoleListCreateView, basename='role')

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),

    # Include address URLs here
    path('', include(router.urls)),  # This will include all the address-related routes

    # Include role URLs here
    # path('', include(role_router.urls)),  # This will include all the role-related routes
]
