from rest_framework import serializers
from .models import *

class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = '__all__'


class ParentMenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentMenus
        fields = '__all__'


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = '__all__'


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'


class UserInfoLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)


class PermissionsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionsUser
        fields = '__all__'


class HotelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwner
        fields = [
            'contact_person_name',
            'hotel_name',
            'email',
            'password',
            'address_location',  # Make sure this matches the model field
            'contact_number',
            'google_map_address'
        ]

    def create(self, validated_data):
        # Hash the password before saving
        hotel_owner = HotelOwner(**validated_data)
        hotel_owner.set_password(validated_data['password'])
        hotel_owner.save()
        return hotel_owner

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'id',
            'hotel_name',
            'email',
            'contact',
            'address',
            'map_url',
            'gst_number',
            'food_gst_percentage',
            'room_gst_percentage',
            'joined_date',
            'hotel_owner'  # Ensure this is the primary key field for the HotelOwner
        ]


class HotelOwnerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class HotelOwnerLoginaSerializer(serializers.Serializer):
    owner = serializers.IntegerField()  # Assuming owner ID is sent as an integer
    token = serializers.CharField(max_length=32)