# Generated by Django 4.0.3 on 2022-10-29 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Customer Confirmed', 'Customer Confirmed'), ('Admin Confirmed', 'Admin Confirmed'), ('In-Transit', 'In-Transit'), ('Delivered', 'Delivered'), ('Return', 'Return'), ('Cancel', 'Cancel')], default='Pending', max_length=200, null=True),
        ),
    ]