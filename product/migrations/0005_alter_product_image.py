# Generated by Django 5.1.4 on 2025-01-13 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_slug_alter_product_stock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='product_images/%Y/%m'),
        ),
    ]
