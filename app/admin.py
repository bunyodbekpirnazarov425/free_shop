from django.contrib import admin
from .models import User
from django.contrib.auth import get_user_model

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'photo', 'is_staff')

    User = get_user_model()