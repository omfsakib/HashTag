# Generated by Django 4.0.3 on 2022-10-02 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_order_cupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cupon_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]