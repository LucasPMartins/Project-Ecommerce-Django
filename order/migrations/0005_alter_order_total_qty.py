# Generated by Django 5.1.4 on 2025-01-17 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_created_at_order_total_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_qty',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
