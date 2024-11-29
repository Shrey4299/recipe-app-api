from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from core.models import Address, User
from user.serializers import AddressSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class AddressViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """ViewSet for managing user addresses."""

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Override to get the address of the current user."""
        user = self.request.user
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        """Override to assign the address to the user when creating or updating."""
        user = self.request.user

        # Check if the user already has an address
        address = Address.objects.filter(user=user).first()

        if address:
            # If an address exists, update the existing one
            print("Updating address for user")  # Debugging log
            serializer.update(address, serializer.validated_data)
            return Response(
                AddressSerializer(address).data,
                status=status.HTTP_200_OK
            )

        # If no address exists, create a new one
        print("Creating new address for user")  # Debugging log
        serializer.save(user=user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )














    # def perform_update(self, serializer):
    #     """Override to add custom logic during update."""
    #     # serializer.save(last_updated_by=self.request.user)

    # def perform_destroy(self, instance):
    #     """Override to perform custom deletion logic."""
    #     # super().perform_destroy(instance)
    #     # # Custom logic after deleting (e.g., log deletion)
    #     # print(f"Address {instance.id} was deleted.")

    # def get_serializer_class(self):
    #     """Override to return a different serializer class based on the action."""
    #     # if self.action == 'create':
    #     #     return CreateAddressSerializer
    #     # return AddressSerializer

    # def get_permissions(self):
    #     """Override to set custom permissions based on action."""

    #     # in built actions are 'list', 'create', 'update', 'delete' ,'retrieve', 'destroy' , 'partially_update'
    #     # if self.action == 'create':
    #     #     return [IsAuthenticated()]
    #     # return [IsAuthenticatedOrReadOnly()]


    # def get_authenticators(self):
    #     """Override to add custom authentication."""
    #     # if self.action == 'create':
    #     #     return [CustomAuthenticator()]
    #     # return super().get_authenticators()





# *******************************************************************************************************
# *******************************************************************************************************




# Common Usage of the Overridden Methods
# These methods provide you with the flexibility to customize the behavior of your ViewSet for different actions. Here are some common scenarios where you might override these methods:

# Custom Querysets: Using get_queryset() to filter records, e.g., returning only the addresses related to the logged-in user.
# Pre-save Logic: Using perform_create() and perform_update() to assign additional data (like the current user) before saving an object.
# Permission Handling: Overriding get_permissions() to set different permissions for different actions.
# Custom Serializers: Using get_serializer_class() to return a different serializer depending on the action.
# Authentication Handling: Overriding get_authenticators() if you want to apply different authentication schemes based on the action.




# *******************************************************************************************************
# *******************************************************************************************************

# Option 2: Without GenericViewSet
# You can also use a simpler approach by directly using individual mixins such as ListModelMixin, CreateModelMixin, and UpdateModelMixin or APIView for more control:


# class AddressCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     """Handle address creation."""
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer

#     def perform_create(self, serializer):
#         """Override to assign the address to the user when creating."""
#         serializer.save(user=self.request.user)

# class AddressListView(mixins.ListModelMixin, viewsets.GenericViewSet):
#     """Handle listing addresses."""
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer

#     def get_queryset(self):
#         """Override to get the address of the current user."""
#         return Address.objects.filter(user=self.request.user)