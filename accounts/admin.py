from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .forms import SignUpForm
from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    list_display = ("username", "email", "full_name", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("full_name", "bio", "location", "profile_picture")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profile", {"fields": ("full_name", "email")}),
    )
