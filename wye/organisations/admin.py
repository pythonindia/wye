from django.contrib import admin

from .models import Organisation


class OrganisationAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'organisation_type',
        'name',
        'location')
    search_fields = (
        'organisation_type',
        'name')
    list_filter = (
        'active',
        'organisation_type',
        'name',
        'location')


admin.site.register(Organisation, OrganisationAdmin)
