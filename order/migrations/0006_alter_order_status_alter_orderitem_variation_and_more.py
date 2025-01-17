# Generated by Django 5.1.4 on 2025-01-17 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_orderitem_variation_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('C', 'Created'), ('R', 'Rejected'), ('P', 'Pending'), ('S', 'Sent'), ('F', 'Finished')], default='Created', max_length=1),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='variation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='variation_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]