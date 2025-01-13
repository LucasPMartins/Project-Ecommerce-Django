from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('user', 'birthday', 'cpf', 'adress', 'number','neighborhood', 'cep', 'city', 'state')
    search_fields = ('user__first_name', 'user__last_name', 'cpf', 'cep', 'city', 'state')
    list_filter = ('state',)
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'birthday', 'cpf')
        }),
        ('Address Information', {
            'fields': ('adress', 'number', 'neighborhood', 'cep', 'city', 'state')
        }),
    )