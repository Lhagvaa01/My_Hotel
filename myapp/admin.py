from django.contrib import admin
from .models import *

@admin.register(SystemInfo)
class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('system_id', 'system_name', 'description')


@admin.register(ParentMenus)
class ParentMenusAdmin(admin.ModelAdmin):
    list_display = ('menu_id', 'menu_name', 'menu_url', 'system_info')


@admin.register(Menus)
class MenusAdmin(admin.ModelAdmin):
    list_display = ('menu_id', 'menu_name', 'menu_url', 'parent_menu', 'system_info')


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_mail', 'user_phone', 'user_type')


@admin.register(PermissionsUser)
class PermissionsUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu', 'can_access')


@admin.register(HotelOwner)
class HotelOwnerAdmin(admin.ModelAdmin):
    list_display = [
        'contact_person_name',
        'hotel_name',
        'address_location',
        'contact_number',
        'email',
        'google_map_address'
    ]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'hotel_owner', 'email', 'contact', 'address', 'joined_date')  # Columns to display in the list view
    search_fields = ('hotel_name', 'hotel_owner__owner_name', 'email')  # Fields to search in the admin interface
    list_filter = ('hotel_owner', 'joined_date')  # Filters to apply in the list view

