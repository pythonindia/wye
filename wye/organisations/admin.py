from django.contrib import admin
from autocomplete_light import shortcuts

from .models import Organisation


class OrganisationAdmin(admin.ModelAdmin):
    form = shortcuts.modelform_factory(Organisation, exclude=[])

admin.site.register(Organisation, OrganisationAdmin)
