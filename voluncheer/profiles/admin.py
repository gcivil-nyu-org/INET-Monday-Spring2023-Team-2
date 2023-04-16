from django.contrib import admin

from profiles.models import Badge
from profiles.models import Organization
from profiles.models import User
from profiles.models import Volunteer

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Volunteer)
admin.site.register(Badge)
