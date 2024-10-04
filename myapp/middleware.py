from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from .models import HotelOwner, UserInfo  # Import UserInfo model
import json


class TokenExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = None

        if request.method == 'POST':
            try:
                body_data = json.loads(request.body)
                token = body_data.get('token')
            except json.JSONDecodeError:
                token = request.POST.get('token')

        if request.method == 'GET':
            token = request.GET.get('token')

        if token:
            try:
                # Handle UserInfo token expiration
                user_info = UserInfo.objects.get(token=token)

                if user_info.token_created_at and timezone.now() > user_info.token_created_at + timedelta(minutes=30):
                    user_info.token = None  # Set token to null after 30 minutes
                    user_info.save()

            except UserInfo.DoesNotExist:
                pass  # Token doesn't belong to any UserInfo instance

            try:
                # Handle HotelOwner token expiration (if needed)
                hotel_owner = HotelOwner.objects.get(token=token)

                if hotel_owner.token_created_at and timezone.now() > hotel_owner.token_created_at + timedelta(
                        minutes=30):
                    hotel_owner.token = None  # Set token to null
                    hotel_owner.save()

            except HotelOwner.DoesNotExist:
                pass  # Token doesn't belong to any HotelOwner instance

        response = self.get_response(request)
        return response
