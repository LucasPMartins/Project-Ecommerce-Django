# Generated by Django 5.1.4 on 2025-01-13 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ItemOrder',
            new_name='OrderItem',
        ),
    ]