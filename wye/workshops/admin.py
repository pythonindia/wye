from django.contrib import admin
from . import models


# class WorkshopAdmin(admin.ModelAdmin):
#     list_per_page = 50
#     list_display = (
#         'requester',
#         'location',
#         'workshop_section',
#         'no_of_participants')
#     search_fields = (
#         'expected_date',
#         'workshop_level',
#         'status')
#     list_filter = ('is_active', 'status', 'workshop_level', 'location')

admin.site.register(models.Workshop)


# class WorkshopFeedBackAdmin(admin.ModelAdmin):
#     pass

admin.site.register(models.WorkshopFeedBack)

admin.site.register(models.WorkshopSections)
admin.site.register(models.WorkshopRatingValues)
admin.site.register(models.WorkshopVoting)
