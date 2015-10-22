from django.contrib import admin
from autocomplete_light import shortcuts

from .models import Location, State


admin.site.register(Location)
admin.site.register(State)
