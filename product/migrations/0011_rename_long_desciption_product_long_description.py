# Generated by Django 5.1.4 on 2025-01-14 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_attributename_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='long_desciption',
            new_name='long_description',
        ),
    ]
