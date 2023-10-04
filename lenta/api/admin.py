from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.v1 import models
from users.forms import CustomUserCreationForm
from users.models import UserStore
from django.contrib.auth import get_user_model
User = get_user_model()


class UserStoreInline(admin.TabularInline):  # Используйте TabularInline для компактного отображения
    model = UserStore
    extra = 1  # Количество дополнительных полей для отображения


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2', 'store'),
        }),
    )
    inlines = [UserStoreInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserStore)
admin.site.register(models.Store)
admin.site.register(models.Product)
admin.site.register(models.Sales)
admin.site.register(models.SalesForecast)