from django.urls import path
from .views import (
    PersonalInfoRegistrationView, SchoolInfoRegistrationView,UserProfileView,
    UserLoginView, UserLogoutView, TokenResetView)

urlpatterns = [
    path('personal-info/', PersonalInfoRegistrationView.as_view(), name='personal-info'),
    path('school-info/', SchoolInfoRegistrationView.as_view(), name='school-info'),
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token-reset/', TokenResetView.as_view(), name='token-reset'),
]

