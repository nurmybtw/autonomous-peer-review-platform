from django.contrib import admin
from .models import User, Publication
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Roles', {'fields': ('is_reviewer', )}),
        ('Password', {'fields': ('password', )}),
    )
    add_fieldsets = (
        ('Roles', {'fields': ('is_reviewer', )}),
        ('Password', {'fields': ('password', )}),
    )


admin.site.register(User, UserAdmin)
# admin.site.register(User)
admin.site.register(Publication)
