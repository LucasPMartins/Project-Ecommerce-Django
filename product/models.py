from django.db import models
from django.conf import settings
from utils.images import resize_image
from utils.rands import new_slugify

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True,default=None, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, 
        default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, 
        default=None, null=True, blank=True)
    long_desciption = models.TextField(max_length=999)
    short_description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='product_images/%Y/%m',blank=True,default='')
    price = models.DecimalField(max_digits=100,decimal_places=2)
    discount_price = models.DecimalField(max_digits=100,decimal_places=2,default=0.00)
    product_type = models.CharField(
        max_length=20,
        choices=[('simple','Simple'),('variable','Variable')],
        default='simple'
        )
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    stock = models.PositiveIntegerField(default=0,help_text='Show the total stock of the product if it is a variable product')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.name)
        if self.product_type == 'variable':
            self.stock = sum([var.stock for var in self.variations.all()])
        super_save = super().save(*args, **kwargs)
        if self.image:
            print(self.image.name)
            self.image = resize_image(self.image)
        return super_save

    def __str__(self):
        return self.name


# Atributo: como "cor" ou "tamanho"
class AttributeName(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Valores possíveis para um atributo (ex.: "azul", "M")
class AttributeValue(models.Model):
    attr = models.ForeignKey(AttributeName, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return f"{self.attr.name}: {self.value}"

# Variação do Produto
class ProductVariation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    attributes = models.ManyToManyField(AttributeValue, related_name="variations")
    stock = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Define o preço padrão como o preço do produto, se não for especificado
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Variation of {self.product.name}"
