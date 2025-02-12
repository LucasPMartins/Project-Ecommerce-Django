from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('id','user', 'birthday', 'cpf', 'address', 'number','neighborhood', 'cep', 'city', 'state')
    list_display_links = ('id', 'user')
    search_fields = ('user__first_name', 'user__last_name', 'cpf', 'cep', 'city', 'state')
    list_filter = ('state',)
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'birthday', 'cpf')
        }),
        ('Address Information', {
            'fields': ('address', 'number', 'neighborhood', 'cep', 'city', 'state')
        }),
    )