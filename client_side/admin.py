from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cart, CartItem

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    ordering = ('email',)

# Unregister CustomUser from any existing admin class
admin.site.unregister(CustomUser)

# Register CustomUser with the customized admin class
admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Cart)
admin.site.register(CartItem)
