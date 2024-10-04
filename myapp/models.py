from django.db import models
from django.contrib.auth.models import User


class SystemInfo(models.Model):
    system_id = models.CharField(max_length=255)
    system_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.system_name


class ParentMenus(models.Model):
    system_info = models.ForeignKey(SystemInfo, on_delete=models.CASCADE)
    menu_id = models.IntegerField()
    menu_name = models.CharField(max_length=255)
    menu_url = models.CharField(max_length=255)

    def __str__(self):
        return self.menu_name


class Menus(models.Model):
    system_info = models.ForeignKey(SystemInfo, on_delete=models.CASCADE)
    menu_id = models.IntegerField()
    menu_name = models.CharField(max_length=255)
    parent_menu = models.ForeignKey(ParentMenus, on_delete=models.CASCADE)
    menu_url = models.CharField(max_length=255)

    def __str__(self):
        return self.menu_name


class PermissionsUser(models.Model):
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)  # Reference UserInfoUser model
    menu = models.ForeignKey('Menus', on_delete=models.CASCADE)
    can_access = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user_name} - {self.menu.menu_name}"


class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    user_name = models.CharField(max_length=255)
    user_pass = models.CharField(max_length=255)
    user_mail = models.EmailField()
    user_phone = models.CharField(max_length=15)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, blank=True, null=True)
    token_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user_name


class HotelOwner(models.Model):
    contact_person_name = models.CharField(max_length=255)
    hotel_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address_location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    google_map_address = models.URLField(blank=True, null=True)
    token = models.CharField(max_length=32, blank=True, null=True)
    token_created_at = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.contact_person_name} - {self.hotel_name}"


class Hotel(models.Model):
    hotel_owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE)  # New field to link HotelOwner
    hotel_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    map_url = models.URLField(null=True, blank=True)
    gst_number = models.CharField(max_length=100, null=True, blank=True)
    food_gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    room_gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    joined_date = models.DateTimeField()

    def __str__(self):
        return self.hotel_name
