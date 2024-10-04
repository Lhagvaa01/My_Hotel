from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'system-info', SystemInfoViewSet)
router.register(r'parent-menus', ParentMenusViewSet)
router.register(r'menus', MenusViewSet)
router.register(r'permissions-user', PermissionsUserViewSet)
router.register(r'user-info', UserInfoViewSet)
router.register(r'user-type', UserTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-user/', create_user_info, name='create_user_info'),
    path('user-info-login/', user_info_login, name='user_info_login'),
    path('create-hotel-owner/', create_hotel_owner, name='create_hotel_owner'),
    path('create-hotel/', create_hotel, name='create_hotel'),
    path('hotels/owner/', get_hotel_owner_hotels, name='hotel-owner-hotels'),
    path('hotel-owner/login/', hotel_owner_login, name='hotel_owner_login'),
]
