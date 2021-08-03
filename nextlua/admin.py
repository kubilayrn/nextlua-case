from django.contrib import admin

# Register your models here.

from nextlua.models import Vehicle ,VehicleModel

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    pass