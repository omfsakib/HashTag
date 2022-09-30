from itertools import product
from .models import *

def productSerialize(id):
    product = Product.objects.get(id = id)

    total_images = ProductImages.objects.filter(product = product).count()
    print(total_images)
    if total_images == 1: 
        product_image_1_loop = ProductImages.objects.filter(product = product)[:1]
        for k in product_image_1_loop:
            product_image_1 = k.img.url

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'description':product.description,
            'date_created':product.date_created,
            'stock':product.stock,
            'discount':product.discount,
            'discount_amount':product.discount_amount,
            'rate':product.rate,
            'featured':product.featured,
            'image_1' : product_image_1,
        }
    elif total_images == 2:
        product_image_1_loop = ProductImages.objects.filter(product = product)[:1]
        for k in product_image_1_loop:
            product_image_1 = k.img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.img.url

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'description':product.description,
            'date_created':product.date_created,
            'stock':product.stock,
            'discount':product.discount,
            'discount_amount':product.discount_amount,
            'rate':product.rate,
            'featured':product.featured,
            'image_1' : product_image_1,
            'image_2' : product_image_2
        }
    elif total_images == 3:
        product_image_1_loop = ProductImages.objects.filter(product = product)[:1]
        for k in product_image_1_loop:
            product_image_1 = k.img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.img.url
        
        product_image_3_loop = ProductImages.objects.filter(product = product)[2:3]
        for k in product_image_3_loop:
            product_image_3 = k.img.url

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'description':product.description,
            'date_created':product.date_created,
            'stock':product.stock,
            'discount':product.discount,
            'discount_amount':product.discount_amount,
            'rate':product.rate,
            'featured':product.featured,
            'image_1' : product_image_1,
            'image_2' : product_image_2,
            'image_3' : product_image_3
        }
    elif total_images == 4:
        product_image_1_loop = ProductImages.objects.filter(product = product)[:1]
        for k in product_image_1_loop:
            product_image_1 = k.img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.img.url
        
        product_image_3_loop = ProductImages.objects.filter(product = product)[2:3]
        for k in product_image_3_loop:
            product_image_3 = k.img.url
        
        product_image_4_loop = ProductImages.objects.filter(product = product)[3:4]
        for k in product_image_4_loop:
            product_image_4 = k.img.url

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'description':product.description,
            'date_created':product.date_created,
            'stock':product.stock,
            'discount':product.discount,
            'discount_amount':product.discount_amount,
            'rate':product.rate,
            'featured':product.featured,
            'image_1' : product_image_1,
            'image_2' : product_image_2,
            'image_3' : product_image_3,
            'image_4' : product_image_4
        }
    elif total_images == 5:
        product_image_1_loop = ProductImages.objects.filter(product = product)[:1]
        for k in product_image_1_loop:
            product_image_1 = k.img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.img.url
        
        product_image_3_loop = ProductImages.objects.filter(product = product)[2:3]
        for k in product_image_3_loop:
            product_image_3 = k.img.url
        
        product_image_4_loop = ProductImages.objects.filter(product = product)[3:4]
        for k in product_image_4_loop:
            product_image_4 = k.img.url
    
        product_image_5_loop = ProductImages.objects.filter(product = product)[4:5]
        for k in product_image_5_loop:
            product_image_5 = k.img.url

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'description':product.description,
            'date_created':product.date_created,
            'stock':product.stock,
            'discount':product.discount,
            'discount_amount':product.discount_amount,
            'rate':product.rate,
            'featured':product.featured,
            'image_1' : product_image_1,
            'image_2' : product_image_2,
            'image_3' : product_image_3,
            'image_4' : product_image_4,
            'image_5' : product_image_5
        }
    return product_with_image