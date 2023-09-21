from django.contrib import admin
from .models import Plant

# Register your models here.
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'botanical_name',)


admin.site.register(Plant, PlantAdmin)