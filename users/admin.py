from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class UserCustomAdmin(UserAdmin):
    list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )


admin.site.register(User, UserCustomAdmin)

from django.contrib.auth.models import Group
# Safely unregister Group model to clean up admin panel
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass
