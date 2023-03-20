from django.contrib import admin
from opportunityboard.models import Category
from opportunityboard.models import Opportunity
from opportunityboard.models import Subcategory
from opportunityboard.models import Subsubcategory

admin.site.register(Opportunity)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Subsubcategory)
