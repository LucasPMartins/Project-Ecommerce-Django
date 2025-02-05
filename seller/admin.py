from django.contrib import admin
from .models import Seller

# Register your models here.

@admin.register(Seller)
class Seller(admin.ModelAdmin):
    list_display = ['id','store_name','user','cnpj',]
    list_display_links = ['id', 'store_name','user',]
    search_fields = ('user__first_name', 'user__last_name', 'cnpj', 'store_cep', 'store_city', 'store_state')
    list_filter = ('store_state',)
