# Generated by Django 5.1.4 on 2025-01-13 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_category_options_alter_attributevalue_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, default='', to='product.category'),
        ),
    ]
