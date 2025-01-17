import re
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.validation import check_cpf
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    cpf = models.CharField(max_length=11,verbose_name='CPF',unique=True)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=30,blank=True)
    neighborhood = models.CharField(max_length=30)
    cep = models.CharField(max_length=8,verbose_name='CEP')
    city = models.CharField(max_length=30)
    state = models.CharField(
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

    def get_age(self):
        if datetime.now().month < self.birthday.month or (datetime.now().month == self.birthday.month and datetime.now().day < self.birthday.day):
            return datetime.now().year - self.birthday.year - 1
        return datetime.now().year - self.birthday.year

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def clean(self):
        error_messages = {}

        if not check_cpf(self.cpf):
            error_messages['cpf'] = 'Type a valid CPF'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'Type a valid CEP'

        current_year = datetime.now().year
        if self.birthday.year < 1900 or self.birthday.year > current_year:
            error_messages['birthday'] = 'Type a valid birthday'

        if error_messages:
            raise ValidationError(error_messages)
        return super().clean()