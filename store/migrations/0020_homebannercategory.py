# Generated by Django 4.0.2 on 2022-10-22 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_latestarrivals_products_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeBannerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_heading', models.CharField(blank=True, max_length=200, null=True)),
                ('sub_title_heading', models.CharField(blank=True, max_length=200, null=True)),
                ('short_description', models.CharField(blank=True, max_length=200, null=True)),
                ('banner_img', models.ImageField(blank=True, default='product-pic.jpg', null=True, upload_to='')),
                ('estimated_category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
        ),
    ]
