from django.urls import path
from .views import HomeView, LoginView, RegisterView, LogoutView, UpdateProfileImageView, UserProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/profile/', UserProfileView.as_view(), name='profile'),
    path('user/profile/update-photo', UpdateProfileImageView.as_view(), name='update_photo'),

]