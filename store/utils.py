import json
import uuid
from .models import *
from django.contrib.auth import login
from django.contrib.auth.models import Group

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
            cartItems += cart[i]["quantity"]
            
            product = Product.objects.get(id = i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']


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

def guestOrder(request,data):
    name = data['form']['name']
    phone = data['form']['phone']
    
    cookieData = cookieCart(request)
    items = cookieData['items']
    
    customer, created = Customer.objects.get_or_create(
        phone = phone,
    )
    if created:
        username = phone
        user = User.objects.create(username= username,first_name = name)
        customer.user = user
        customer.save()
        auth_token=str(uuid.uuid4())
        profile_obj = UserProfile.objects.create(user = user,auth_token=auth_token)
        profile_obj.save()
        group = Group.objects.get(name = 'customer')
        user.groups.add(group)
        login(request,user)
    else:
        user = customer.user
        login(request,user)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        shopowner = product.shopowner
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.shop.add(shopowner)
        quantity = item['quantity']
        rate = product.price
        total = float(product.price) * float(quantity)
        orderItem = OrderItem.objects.get_or_create(
            product=product,
            order = order,
            customer=customer, 
            shop=shopowner,
            quantity = item['quantity'],
            size = item['size'],
            color = item['color'],
            rate = rate,
            total = total
            )
    return customer,order