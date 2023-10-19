from django.contrib import admin
from .models import Plant, Disease


# Register your models here.
class DiseaseInline(admin.TabularInline):
    model = Disease


class PlantAdmin(admin.ModelAdmin):
    inlines = [DiseaseInline]

    list_display = (
        "name",
        "botanical_name",
    )


admin.site.register(Plant, PlantAdmin)
