# Generated by Django 5.1.4 on 2025-01-13 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]