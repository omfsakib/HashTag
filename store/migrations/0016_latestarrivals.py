# Generated by Django 4.0.3 on 2022-10-09 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_orderitem_status_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestArrivals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='store.product')),
            ],
        ),
    ]
