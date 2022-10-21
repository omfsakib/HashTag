import json
import uuid
from .models import *
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login

def productSerialize(id):
    product = Product.objects.get(id = id)

    total_images = ProductImages.objects.filter(product = product).count()
    if total_images == 1: 
        product_image_1_loop = ProductImages.objects.filter(product = product)[:1]
        for k in product_image_1_loop:
            product_image_1 = k.n_img.url
        
        sizes = product.size.all()
        if sizes:
            first_size_loop = sizes[:1]
            for i in first_size_loop:
                first_size = i.size
        
        color = product.color.all()
        if color:
            first_color_loop = color[:1]
            for i in first_color_loop:
                first_color = i.color

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'color':color,
            'first_color':first_color,
            'size':sizes,
            'first_size':first_size,
            'product_code':product.product_code,
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
            product_image_1 = k.n_img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.n_img.url

        sizes = product.size.all()
        if sizes:
            first_size_loop = sizes[:1]
            for i in first_size_loop:
                first_size = i.size

        color = product.color.all()
        if color:
            first_color_loop = color[:1]
            for i in first_color_loop:
                first_color = i.color

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'color':color,
            'first_color':first_color,
            'size':sizes,
            'first_size':first_size,
            'product_code':product.product_code,
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
            product_image_1 = k.n_img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.n_img.url
        
        product_image_3_loop = ProductImages.objects.filter(product = product)[2:3]
        for k in product_image_3_loop:
            product_image_3 = k.n_img.url

        sizes = product.size.all()
        if sizes:
            first_size_loop = sizes[:1]
            for i in first_size_loop:
                first_size = i.size

        color = product.color.all()
        if color:
            first_color_loop = color[:1]
            for i in first_color_loop:
                first_color = i.color

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'color':color,
            'first_color':first_color,
            'size':sizes,
            'first_size':first_size,
            'product_code':product.product_code,
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
            product_image_1 = k.n_img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.n_img.url
        
        product_image_3_loop = ProductImages.objects.filter(product = product)[2:3]
        for k in product_image_3_loop:
            product_image_3 = k.n_img.url
        
        product_image_4_loop = ProductImages.objects.filter(product = product)[3:4]
        for k in product_image_4_loop:
            product_image_4 = k.n_img.url

        sizes = product.size.all()
        if sizes:
            first_size_loop = sizes[:1]
            for i in first_size_loop:
                first_size = i.size

        color = product.color.all()
        if color:
            first_color_loop = color[:1]
            for i in first_color_loop:
                first_color = i.color

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'color':color,
            'first_color':first_color,
            'size':sizes,
            'first_size':first_size,
            'product_code':product.product_code,
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
            product_image_1 = k.n_img.url

        product_image_2_loop = ProductImages.objects.filter(product = product)[1:2]
        for k in product_image_2_loop:
            product_image_2 = k.n_img.url
        
        product_image_3_loop = ProductImages.objects.filter(product = product)[2:3]
        for k in product_image_3_loop:
            product_image_3 = k.n_img.url
        
        product_image_4_loop = ProductImages.objects.filter(product = product)[3:4]
        for k in product_image_4_loop:
            product_image_4 = k.n_img.url
    
        product_image_5_loop = ProductImages.objects.filter(product = product)[4:5]
        for k in product_image_5_loop:
            product_image_5 = k.n_img.url

        sizes = product.size.all()
        if sizes:
            first_size_loop = sizes[:1]
            for i in first_size_loop:
                first_size = i.size

        color = product.color.all()
        if color:
            first_color_loop = color[:1]
            for i in first_color_loop:
                first_color = i.color

        product_with_image = {
            'id':product.id,
            'name':product.name,
            'price':product.price,
            'category':product.category.all(),
            'color':color,
            'first_color':first_color,
            'size':sizes,
            'first_size':first_size,
            'product_code':product.product_code,
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

def cookieCart(request):  
    try:
        cupon_d = json.loads(request.COOKIES.get('cupon'))
        cupon_code = cupon_d['cupon_code']
        cupon_exits = Cupon.objects.filter(cupon_code = cupon_code).count()
        if cupon_exits == 1:
            cupon_object = Cupon.objects.get(cupon_code = cupon_code)
            cupon = cupon_object.cupon_code
            amount = cupon_object.amount
        else:
            cupon = "None"
            amount = 0
    except:
        
        cupon = "None"
        amount = 0

    try:
        cart = json.loads(request.COOKIES.get('cart'))
       
    except: 
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False,'cupon_code':cupon,'cupon_amount':amount}
    cartItems = order['get_cart_items']
    cartTotal = order['get_cart_total']

    
    for i in cart :
        try:
            cartItems += int(cart[i]["quantity"])
            
            product = Product.objects.get(id = i)
            total = float((float(product.price) * int(cart[i]['quantity'])))
            order['get_cart_total'] += total
            order['get_cart_items'] += int(cart[i]['quantity'])
            print(order['get_cart_items'])


            cartTotal = order['get_cart_total']
            
            
            if 'color' in cart[i]:
                color = cart[i]['color']
            else:
                color = "undefined"

            if 'size' in cart[i]:
                size = cart[i]['size']
                first_size = size
            else:
                size = "undefined"
                first_size = size

            item = {
                'product' : {
                    'id' : product.id,
                    'name': product.name,
                    'price': product.price,
                },
                'quantity' : cart[i]["quantity"],
                'get_total': total,
                'color': color,
                'size': size,
                'first_size':first_size
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
    
    
        except:
            pass
    
    return {"order":order,"items":items,"cartItems":cartItems,'cartTotal':cartTotal}


def checkout_login_handle(request):
    login_username = request.POST.get('login_username')
    password = request.POST.get('login_password')

    try:
        user_1 = User.objects.get(username = login_username)
        username = user.username
    except:
        customer_1 = Customer.objects.get(phone = login_username)
        user_1 =  customer_1.user
        username = user_1.username

    user = authenticate(request,username=username, password=password)
    print(user)

def category_with_products(id):
    categoryProducts = []
    category = Category.objects.get(id = id)
    products = Product.objects.filter(category = category)
    total_product = products.count()
    for i in products:
        product = productSerialize(i.id)
        categoryProducts.append(product)

    categoryWithProducts = {
        'id':category.id,
        'name':category.name,
        'hasProducts':total_product,
        'categoryProducts':categoryProducts
    }
    return categoryWithProducts

def reviews_with_images(id):
    images = []
    tmp_review = Review.objects.get(id = id)
    tmp_date = tmp_review.created_at.date()
    tmp_images = ReviewImages.objects.filter(review = tmp_review)
    for i in tmp_images:
        images.append(i.img.url)
    
    review = {
        'id' : tmp_review.id,
        'user': tmp_review.user,
        'product': tmp_review.product,
        'comment': tmp_review.comment,
        'rate': tmp_review.rate,
        'created_at':tmp_date,
        'images': images,
    }
    return review
