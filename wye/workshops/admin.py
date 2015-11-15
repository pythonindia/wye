from django.contrib import admin
#from .models import Workshop, WorkshopFeedBack, WorkshopSections
from . import models


class WorkshopAdmin(admin.ModelAdmin):
    list_per_page = 50
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

admin.site.register(models.Workshop, WorkshopAdmin)


class WorkshopFeedBackAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.WorkshopFeedBack, WorkshopFeedBackAdmin)

admin.site.register(models.WorkshopSections)
admin.site.register(models.WorkshopRatingValues)
admin.site.register(models.WorkshopVoting)
