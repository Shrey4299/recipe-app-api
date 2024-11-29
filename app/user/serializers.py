"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from core.models import Address, Role


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street_address', 'city', 'state', 'postal_code', 'country']
        read_only_fields = ['user','id']

class RoleSerializer(serializers.ModelSerializer):
    """Serializer for the Role model."""

    class Meta:
        model = Role
        fields = ['id', 'role_key', 'role_name', 'user']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    address = AddressSerializer(required=False)  # Ensure address is handled correctly

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'address']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password and address."""
        address_data = validated_data.pop('address', None)  # Extract address data if provided
        user = get_user_model().objects.create_user(**validated_data)

        # Create and assign address if provided
        if address_data:
            Address.objects.create(user=user, **address_data)

        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        address_data = validated_data.pop('address', None)  # Extract address data if provided
        password = validated_data.pop('password', None)

        # Update user details
        user = super().update(instance, validated_data)

        # Update password if provided
        if password:
            user.set_password(password)
            user.save()

        # Update address if provided
        if address_data:
            # Update the existing address or create a new one
            address, created = Address.objects.update_or_create(user=user, defaults=address_data)

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


