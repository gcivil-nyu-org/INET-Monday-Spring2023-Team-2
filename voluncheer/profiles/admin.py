from django.contrib import admin
from profiles.models import Badge, Organization, User, Volunteer

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Volunteer)
admin.site.register(Badge)
