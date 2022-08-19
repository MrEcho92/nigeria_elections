from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect


class AdminSite(admin.AdminSite):
    def login(self, *args, **kwargs):
        if settings.DEBUG:
            return redirect(settings.LOGIN_URL)
        return super().login(*args, **kwargs)


admin_site = AdminSite()
