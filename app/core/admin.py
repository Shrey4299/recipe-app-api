"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'phone_number', 'is_active', 'is_staff', 'registered', 'image_uploaded', 'experience']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'phone_number', 'experience')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Other Info'), {'fields': ('registered', 'image_uploaded')}),
    )

    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'phone_number',
                'experience',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )



@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin view for the Address model."""
    list_display = ('user', 'street_address', 'city', 'state', 'country')
    search_fields = ('user__email', 'city', 'state', 'country')
    list_filter = ('city', 'state', 'country')

@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role_key', 'role_name')  # Fields to display in the list view
    search_fields = ('user__email', 'role_key', 'role_name')  # Add search functionality
    list_filter = ('role_key', 'role_name')  # Add filters for better filtering

# Register the Role model with the custom admin class
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)