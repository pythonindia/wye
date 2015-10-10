from django.contrib import admin
from .models import Organisation, OrganisationType, Location, State

admin.site.register(Organisation)
admin.site.register(OrganisationType)
admin.site.register(Location)
admin.site.register(State)
