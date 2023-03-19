from django.contrib import admin
from opportunityboard.models import Category, Opportunity, Subcategory, Subsubcategory

admin.site.register(Opportunity)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Subsubcategory)
