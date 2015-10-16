from django.contrib import admin
from .models import Workshop


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        'requester', 'location',
        'workshop_section', 'no_of_participants')
