# Generated by Django 4.0.2 on 2022-10-22 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_alter_blog_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]