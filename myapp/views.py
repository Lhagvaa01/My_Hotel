import hashlib

from django.utils import timezone

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, permission_classes

from .models import *
from .serializers import *


class SystemInfoViewSet(viewsets.ModelViewSet):
    queryset = SystemInfo.objects.all()
    serializer_class = SystemInfoSerializer


class ParentMenusViewSet(viewsets.ModelViewSet):
    queryset = ParentMenus.objects.all()
    serializer_class = ParentMenusSerializer


class MenusViewSet(viewsets.ModelViewSet):
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


@api_view(['POST'])
def create_user_info(request):
    if request.method == 'POST':
        owner_id = request.data.get('owner')
        token = request.data.get('token')

        # Fetch the hotel owner instance
        try:
            hotel_owner = HotelOwner.objects.get(pk=owner_id)
        except HotelOwner.DoesNotExist:
            return Response({"error": "Hotel owner not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate the token
        if token != hotel_owner.token:  # Adjust this line based on your actual token storage
            return Response({"error": "You do not have permission to access this resource."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token():
    return get_random_string(32)


@api_view(['POST'])
def user_info_login(request):
    serializer = UserInfoLoginSerializer(data=request.data)

    if serializer.is_valid():
        user_mail = serializer.validated_data['email']
        user_pass = serializer.validated_data['password']

        # Use get() instead of filter() to retrieve a single user instance
        try:
            user = UserInfo.objects.get(user_mail=user_mail)  # Use get() to find a single user

            # Check if the hashed password matches
            if user.user_pass == user_pass:  # Check the hashed password
                # Generate token
                token = generate_token()

                # Save the token and timestamp in the user instance
                user.token = token
                user.token_created_at = timezone.now()  # Set the current timestamp
                user.save()

                # Return success response with token
                return Response({
                    'message': 'Login successful',
                    'token': token,
                    'user': {
                        'user_name': user.user_name,
                        'user_mail': user.user_mail,
                        'user_phone': user.user_phone,
                        'user_type': user.user_type.id
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        except UserInfo.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PermissionsUserViewSet(viewsets.ModelViewSet):
    queryset = PermissionsUser.objects.all()
    serializer_class = PermissionsUserSerializer


@api_view(['POST'])
def create_hotel_owner(request):
    serializer = HotelOwnerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_hotel(request):
    owner_id = request.data.get('hotel_owner')
    token = request.data.get('token')

    # Fetch the hotel owner instance
    try:
        hotel_owner = HotelOwner.objects.get(pk=owner_id)
    except HotelOwner.DoesNotExist:
        return Response({"error": "Hotel owner not found."}, status=status.HTTP_404_NOT_FOUND)

    # Validate the token
    if token != hotel_owner.token:  # Adjust this line based on your actual token storage
        return Response({"error": "You do not have permission to access this resource."},
                        status=status.HTTP_403_FORBIDDEN)

    hotel_owner_id = request.data.get('hotel_owner')
    if not hotel_owner_id:
        return Response({"error": "Hotel owner ID is required"}, status=400)

    try:
        hotel_owner = HotelOwner.objects.get(pk=hotel_owner_id)
    except HotelOwner.DoesNotExist:
        return Response({"error": "Hotel owner not found"}, status=404)

    hotel_data = request.data.copy()
    hotel_data['hotel_owner'] = hotel_owner.pk  # Pass as an ID

    serializer = HotelSerializer(data=hotel_data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Hotel created successfully!', 'data': serializer.data}, status=201)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def get_hotel_owner_hotels(request):
    serializer = HotelOwnerLoginaSerializer(data=request.data)

    # Validate the incoming data
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Safe to access validated_data
    owner_id = serializer.validated_data['owner']
    token = serializer.validated_data['token']

    # Fetch the hotel owner instance
    try:
        hotel_owner = HotelOwner.objects.get(pk=owner_id)
    except HotelOwner.DoesNotExist:
        return Response({"error": "Hotel owner not found."}, status=status.HTTP_404_NOT_FOUND)

    # Validate the token
    if token != hotel_owner.token:  # Adjust this line based on your actual token storage
        return Response({"error": "You do not have permission to access this resource."},
                        status=status.HTTP_403_FORBIDDEN)

    # Fetch the hotels associated with the owner
    hotels = Hotel.objects.filter(hotel_owner=hotel_owner)
    hotel_serializer = HotelSerializer(hotels, many=True)
    return Response(hotel_serializer.data)


def generate_token():
    return get_random_string(32)

@api_view(['POST'])
def hotel_owner_login(request):
    serializer = HotelOwnerLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            hotel_owner = HotelOwner.objects.get(email=email)

            if hotel_owner.check_password(password):
                # Generate a new token
                token = generate_token()

                # Update the token and the created timestamp
                hotel_owner.token = token
                hotel_owner.token_created_at = timezone.now()  # Set the current timestamp
                hotel_owner.save()

                return Response({
                    'message': 'Login successful',
                    'token': token,
                    'hotel_owner': {
                        'contact_person_name': hotel_owner.contact_person_name,
                        'hotel_name': hotel_owner.hotel_name,
                        'email': hotel_owner.email,
                        'contact_number': hotel_owner.contact_number,
                        'address_location': hotel_owner.address_location,
                        'google_map_address': hotel_owner.google_map_address
                    }
                }, status=status.HTTP_200_OK)

            else:
                return Response({'non_field_errors': ['Invalid password.']}, status=status.HTTP_400_BAD_REQUEST)
        except HotelOwner.DoesNotExist:
            return Response({'non_field_errors': ['HotelOwner with this email does not exist.']}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

