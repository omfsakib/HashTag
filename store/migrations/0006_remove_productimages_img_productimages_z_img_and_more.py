# Generated by Django 4.0.2 on 2022-10-01 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_color_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimages',
            name='img',
        ),
        migrations.AddField(
            model_name='productimages',
            name='Z_img',
            field=models.ImageField(blank=True, default='product-pic.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='productimages',
            name='n_img',
            field=models.ImageField(blank=True, default='product-pic.jpg', null=True, upload_to=''),
        ),
    ]
