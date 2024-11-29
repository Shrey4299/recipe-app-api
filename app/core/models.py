"""
Database models.
"""
from enum import Enum
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)

class RoleKey(Enum):
    CK = 'CK'  # Cook
    NL = 'NL'  # Normal
    SA = 'SA'  # Super Admin
    MANAGER = 'MANAGER'  # Manager


class RoleName(Enum):
    COOK = 'COOK'
    NORMAL = 'NORMAL'
    SUPER_ADMIN = 'SUPER ADMIN'
    MANAGER = 'MANAGER'

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # Unique phone number
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)  # Registered status (default: False)
    image_uploaded = models.BooleanField(default=False)  # Image uploaded status (default: False)
    experience = models.FloatField(default=0.0)  # Experience in years, default is 0.0

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Address(models.Model):
    """Address for each user."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.state}, {self.country}'

class Role(models.Model):
    """Role for each user."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # Using Enum for role_key and role_name with choices
    role_key = models.CharField(
        max_length=255,
        choices=[(tag, tag.value) for tag in RoleKey],  # Choices for role_key
        default=RoleKey.NL.value  # Default role_key as "NL" (Normal)
    )

    role_name = models.CharField(
        max_length=255,
        choices=[(tag, tag.value) for tag in RoleName],  # Choices for role_name
        default=RoleName.NORMAL.value  # Default role_name as "NORMAL" (Normal Role)
    )

    def __str__(self):
        return f'{self.user}, {self.role_name}'

class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name






