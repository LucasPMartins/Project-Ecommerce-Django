from django.db import models

from utils.rands import new_slugify

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True,default=None, null=True, blank=True)
    slug = models.SlugField(max_length=150,unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class ProductType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150,unique=True,default=None, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    long_desciption = models.TextField(max_length=999)
    short_description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='product/images/%Y/%m',blank=True,default='')
    slug = models.SlugField(max_length=150,unique=True)
    price = models.DecimalField(decimal_places=2)
    discount_price = models.DecimalField(decimal_places=2,default=0.00)
    product_type = ...
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)


