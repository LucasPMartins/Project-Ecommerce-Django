# Generated by Django 5.1.4 on 2025-01-14 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_itemorder_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Order Item', 'verbose_name_plural': 'Order Items'},
        ),
    ]
