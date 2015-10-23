from django.contrib import admin

from .models import Location, State


class LocationAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        'name',
        'state')
    search_fields = ('name',)
    list_filter = (
        'name',
        'state')


class StateAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('name',)

admin.site.register(Location, LocationAdmin)
admin.site.register(State, StateAdmin)
