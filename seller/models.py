from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    store_name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14,verbose_name='CNPJ',unique=True)
    store_address = models.CharField(max_length=50)
    store_number = models.CharField(max_length=5)
    store_complement = models.CharField(max_length=30,blank=True)
    store_neighborhood = models.CharField(max_length=30)
    store_cep = models.CharField(max_length=8,verbose_name='CEP')
    store_city = models.CharField(max_length=30)
    comercial_number = models.CharField(max_length=11)
    store_state = models.CharField(
        max_length=2,
        default='MG',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )
    def __str__(self):
        return f'{self.user}'