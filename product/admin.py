from django.contrib import admin
from . import models

class ProductVariationInline(admin.TabularInline):
    model = models.ProductVariation
    extra = 1  # Número de variações extras exibidas por padrão
    fields = ('price','discount_price', 'attributes', 'stock')  # Campos que serão exibidos no inline
    autocomplete_fields = ('attributes',)  

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name',]
    list_display_links = ['id','name',]
    search_fields = ('id','name',)
    list_per_page = 10
    ordering = ('-id',)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','get_formatted_price','get_formatted_discount_price','stock']
    list_display_links = ['id','name']
    search_fields = ('id','name', 'slug')
    list_per_page = 10
    ordering = ('-id',)
    prepopulated_fields = {'slug':('name',)}

    def get_inlines(self, request, obj):
        if obj and obj.product_type == 'variable':
            return [ProductVariationInline]
        return []

@admin.register(models.AttributeName)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['id','name']
    search_fields = ('id','name')
    list_per_page = 10
    ordering = ('-id',)

@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['id','attr','value']
    search_fields = ('attr','value')
    list_display_links = ['id']
    list_per_page = 10
    ordering = ('-id',)

@admin.register(models.ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['id','product','get_fomatted_price','get_fomatted_discount_price','stock']
    list_display_links = ['id','product']