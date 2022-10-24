# Generated by Django 4.0.3 on 2022-10-24 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_subscription_alter_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
    ]