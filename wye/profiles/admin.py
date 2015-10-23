from django.contrib import admin
from .models import Profile, UserType

class ProfileAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = (
		'user',
		'slug',
		'mobile')
	search_fields = ('slug',)
	list_filter = (
		'slug',
		'interested_locations',
		'interested_sections')

class UserTypeAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = (
		'display_name',
		'slug',
		'active')
	search_fields = ('slug', 'display_name')
	list_filter = (
		'active',
		'slug')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserType, UserTypeAdmin)
