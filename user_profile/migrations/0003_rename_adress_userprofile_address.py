# Generated by Django 5.1.4 on 2025-01-17 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_userprofile_complement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='adress',
            new_name='address',
        ),
    ]
