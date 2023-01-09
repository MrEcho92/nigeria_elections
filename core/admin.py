from djangae.contrib.googleauth.models import Group, User, UserPermission
from djangae.environment import is_production_environment
from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect

from .models import User as AnalyticsUser


class AdminSite(admin.AdminSite):
    def login(self, *args, **kwargs):
        if settings.DEBUG:
            return redirect(settings.LOGIN_URL)
        elif is_production_environment():
            return redirect(settings.LOGIN_URL)
        else:
            return super().login(*args, **kwargs)


admin_site = AdminSite()

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(UserPermission)

admin_site.register(Group)
admin_site.register(UserPermission)


@admin.register(AnalyticsUser, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
