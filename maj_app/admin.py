from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(plants)
class plantsAdmin(admin.ModelAdmin):
    list_display = ('Name','description','image','discount_price','mrp','discount','rate','start_date','end_date')

@admin.register(cart)
class cartAdmin(admin.ModelAdmin):
    list_display = ('uid','pid','qty')