"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions, mixins, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from core.models import Address
from .serializers import AddressSerializer

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    AddressSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user



class AddressViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """ViewSet for managing user addresses."""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        """Override to get the address of the current user."""
        user = self.request.user
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        """Override to assign the address to the user when creating."""
        serializer.save(user=self.request.user)