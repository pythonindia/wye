from django.contrib import admin
from .models import Profile, UserType


class ProfileAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'user',
        'mobile')
    search_fields = ('user__username', 'mobile')
    list_filter = (
        'interested_locations',
        'interested_sections')


class UserTypeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'display_name',
        'active')
    search_fields = ('user__username', 'display_name')
    list_filter = (
        'active',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserType, UserTypeAdmin)
