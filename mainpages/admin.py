from django.contrib import admin
from mainpages.models import Categories,SpentModel


# Register your models here.
class AdminCategories(admin.ModelAdmin):
    list_display = ('title', 'user')

class AdminSpent(admin.ModelAdmin):
    list_display = ('title', 'user','category')

admin.site.register(Categories, AdminCategories)
admin.site.register(SpentModel, AdminSpent)
