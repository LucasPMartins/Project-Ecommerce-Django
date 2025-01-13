from django.contrib import admin
from .models import Order, ItemOrder

class ItemOrderInline(admin.TabularInline):
    model = ItemOrder
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status')
    inlines = [ItemOrderInline]

@admin.register(ItemOrder)
class ItemOrderAdmin(admin.ModelAdmin):
    pass