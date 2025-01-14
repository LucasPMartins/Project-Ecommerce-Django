from django.db import models
from utils.images import resize_image
from django.utils.text import slugify
from utils import format

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=100,unique=True,default=None, null=True, blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, 
        default=None, null=True, blank=True)
    long_description = models.TextField(max_length=999)
    short_description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='product_images/%Y/%m',blank=True,default='')
    price = models.DecimalField(max_digits=100,decimal_places=2)
    discount_price = models.DecimalField(max_digits=100,decimal_places=2,default=0.00)
    product_type = models.CharField(
        max_length=20,
        choices=[('simple','Simple'),('variable','Variable')],
        default='simple'
        )
    category = models.ManyToManyField(Category,blank=True)
    stock = models.PositiveIntegerField(default=0,help_text='Show the total stock of the product if it is a variable product')

    def get_formatted_price(self):
        return format.format_price(self.price)
    get_formatted_price.short_description = 'Price'
    def get_formatted_discount_price(self):
        return format.format_price(self.discount_price)
    get_formatted_discount_price.short_description = 'Discount Price'


    def save(self, *args, **kwargs):
        current_image_name = str(self.image.name)
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = f'{slugify(self.name)}-{self.id}'

        if self.product_type == 'variable':
            if self.variations:
                self.stock = sum([var.stock for var in self.variations.all()])
                self.price = self.variations.first().price
                self.discount_price = self.variations.first().discount_price

        image_changed = False
        if self.image:
            image_changed = current_image_name != self.image.name
        if image_changed:
            resize_image(self.image, new_width=900,quality=70)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Atributo: como "cor" ou "tamanho"
class AttributeName(models.Model):
    class Meta:
        verbose_name = "Attribute Name"
        verbose_name_plural = "Attribute Names"
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Valores possíveis para um atributo (ex.: "azul", "M")
class AttributeValue(models.Model):
    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
    attr = models.ForeignKey(AttributeName, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return f"{self.attr.name}: {self.value}"

# Variação do Produto
class ProductVariation(models.Model):
    class Meta:
        verbose_name = "Product Variation"
        verbose_name_plural = "Product Variations"
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=100,decimal_places=2,default=0.00)
    attributes = models.ManyToManyField(AttributeValue, related_name="variations")
    stock = models.PositiveIntegerField(default=0)

    def get_fomatted_price(self):
        return format.format_price(self.price)
    get_fomatted_price.short_description = "Price"
    def get_fomatted_discount_price(self):
        return format.format_price(self.discount_price)
    get_fomatted_discount_price.short_description = "Discount Price"

    def save(self, *args, **kwargs):
        # Define o preço padrão como o preço do produto, se não for especificado
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Variation of {self.product.name}"
