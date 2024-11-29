from rest_framework import serializers
from core.models import User, Address


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    full_name = serializers.SerializerMethodField()  # Custom computed field
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'address', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
        }

    # Overriding the `create` method
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    # Overriding the `update` method
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    # Overriding the `validate` method for object-level validation
    def validate(self, data):
        """Ensure email is unique."""
        email = data.get('email', None)
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return data

    # Overriding the `validate_<field_name>` method for field-level validation
    def validate_name(self, value):
        """Ensure name has at least two words."""
        if len(value.split()) < 2:
            raise serializers.ValidationError("Name must contain at least two words.")
        return value

    # Overriding the `to_representation` method for customizing output
    def to_representation(self, instance):
        """Customize serialized data."""
        data = super().to_representation(instance)
        data['role'] = 'Admin' if instance.is_superuser else 'User'  # Adding a dynamic field
        return data

    # Overriding the `to_internal_value` method for custom deserialization
    def to_internal_value(self, data):
        """Customize input data before validation."""
        if 'email' in data:
            data['email'] = data['email'].lower()  # Normalize email to lowercase
        return super().to_internal_value(data)

    # Overriding the `run_validation` method for additional validation logic
    def run_validation(self, data):
        """Perform extra validation before main validation."""
        if 'email' not in data:
            raise serializers.ValidationError({'email': "Email is required."})
        return super().run_validation(data)

    # Overriding the `is_valid` method for custom validation logic
    def is_valid(self, raise_exception=False):
        """Customize how validation is triggered."""
        print("Running validation...")  # Debug log
        return super().is_valid(raise_exception=raise_exception)

    # Adding a computed field using `get_<field_name>`
    def get_full_name(self, obj):
        """Return the full name of the user."""
        return f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else obj.name
