from django.contrib import admin
from .models import Part, Compatibility, Category, Order

admin.site.site_header = 'BasmaInventory Dashboard'

class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ['category']

admin.site.register(Part, PartAdmin)
admin.site.register(Compatibility)
admin.site.register(Category)
admin.site.register(Order)
