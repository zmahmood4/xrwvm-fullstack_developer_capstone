from django.contrib import admin
from .models import CarMake, CarModel


# Inline for CarModel
class CarModelInline(
    admin.TabularInline
):  # You can also use `StackedInline` instead of `TabularInline`
    model = CarModel
    extra = 1  # Number of empty forms to display initially


# Admin for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")  # Fields to display in list view
    search_fields = ("name",)  # Search functionality by car make name
    inlines = [CarModelInline]  # Include the inline form for CarModel


# Admin for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "car_make",
        "type",
        "year",
    )  # Fields to display in list view
    search_fields = ("name", "car_make__name")  # Search by model name or car make name
    list_filter = ("type", "year")  # Filter options for easier browsing


# Register models with custom admins
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
