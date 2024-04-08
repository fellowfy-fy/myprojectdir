from django.contrib import admin
from .models import Car, Order

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'vin')
    ordering = ('brand',)
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'car', 'name', 'start_date')
    ordering = ('user',)