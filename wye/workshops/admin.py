from django.contrib import admin
from .models import Workshop

class WorkshopAdmin(admin.ModelAdmin):
	list_per_page = 10
	list_display = (
		'requester',
		'location',
		'workshop_section',
		'no_of_participants')
	fields = ('is_active', 'status')
	search_fields = (
		'expected_date',
		'workshop_level',
		'status')
	list_filter = ('is_active', 'status', 'workshop_level', 'location')

admin.site.register(Workshop, WorkshopAdmin)