from django.contrib import admin

from . import models


class WorkshopAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'requester',
        'workshop_section',
        'no_of_participants')
    search_fields = (
        'expected_date',
        'workshop_level',
        'status')
    list_filter = ('is_active', 'status', 'workshop_level')


class WorkshopFeedBackAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'workshop',
        'feedback_type',
        'comment')
    search_fields = (
        'expected_date',
        'workshop_level',
        'status')
    list_filter = ('feedback_type',)


admin.site.register(models.Workshop, WorkshopAdmin)
admin.site.register(models.WorkshopFeedBack, WorkshopFeedBackAdmin)
admin.site.register(models.WorkshopSections)
admin.site.register(models.WorkshopRatingValues)
admin.site.register(models.WorkshopVoting)
