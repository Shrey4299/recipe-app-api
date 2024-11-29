# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
# from core.models import Role, User
# from user.serializers import RoleSerializer
# from django.shortcuts import get_object_or_404

# class RoleListCreateView(generics.ListCreateAPIView):
#     """View to list and create roles."""
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """Override to return roles related to the current user."""
#         return Role.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         """Assign the role to the current user."""
#         serializer.save(user=self.request.user)

# class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
#     """View to retrieve, update, or delete a role."""
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         """Override to retrieve the role of the current user."""
#         return get_object_or_404(Role, user=self.request.user)
