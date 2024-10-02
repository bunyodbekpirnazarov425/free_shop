from django.urls import path
from .views import (HomeView, LoginView, RegisterView, LogoutView, UpdateProfileImageView,
                    UserProfileView, CustomChangePasswordView)

from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/profile/', UserProfileView.as_view(), name='profile'),
    path('user/profile/update-photo', UpdateProfileImageView.as_view(), name='update_photo'),
    path('user/profile/change-password/', CustomChangePasswordView.as_view(), name='change_password'),

    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]