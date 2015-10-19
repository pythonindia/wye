from django.contrib import admin
from autocomplete_light import shortcuts

from .models import Organisation, Location, State


class OrganisationAdmin(admin.ModelAdmin):
    form = shortcuts.modelform_factory(Organisation, exclude=[])

admin.site.register(Organisation, OrganisationAdmin)

admin.site.register(Location)
admin.site.register(State)
