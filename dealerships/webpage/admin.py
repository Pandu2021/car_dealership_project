from django.contrib import admin
from .models import CarMake, CarModel
from django.contrib.admin.actions import delete_selected

admin.site.register(CarMake)
admin.site.register(CarModel)

class CarMakeAdmin(admin.ModelAdmin):
    actions = [delete_selected]

# Register your models here.
