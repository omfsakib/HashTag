
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import *
from .utils import *
import math
import json
import datetime

# Create your views here.

def logoutUser(request):
    logout(request)
    return redirect('store:home')

def loginUser(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    cartTotal = cookieData['cartTotal']
    order = cookieData['order']
    items = cookieData['items']
    if request.method =='POST' and 'login_username' in request.POST:
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
        if user is not None:
            customer = Customer.objects.get(phone = login_username)
            shipping = ShippingAddress.objects.get(customer = customer)
            db_order, created = Order.objects.get_or_create(customer=customer, complete=False)
            db_order.cupon_code = order['cupon_code']
            db_order.cupon_amount = order['cupon_amount']
            db_order.save()
            shipping.order.add(db_order)
            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                quantity = item['quantity']
                rate = product.price
                total = float(product.price) * float(quantity)
                orderItem = OrderItem.objects.get_or_create(
                    product=product,
                    order = db_order,
                    customer=customer, 
                    quantity = item['quantity'],
                    size = item['size'],
                    color = item['color'],
                    rate = rate,
                    total = total
                    )
            login(request,user)
        return redirect('store:home')
    context = {
        'cartItems':cartItems,
        'cartTotal':cartTotal
    }
    return render(request,'store/login.html',context)

def signUpUser(request):

    context ={

    }
    return render(request,'store/registration.html',context)

def home(request):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()


    total_products = Product.objects.all().count()
    if total_products > 0:

        # Most Viewed Section
        mostViewedCategoryObject = IndivitualCategory.objects.get(category_for = 'mvcategory')
        mostViewedCategorys = mostViewedCategoryObject.categorys.all()
        mostViewedfilterdProductsWithCategorys = []
        for k in mostViewedCategorys:
            mostViewedProducts = Product.objects.filter(category = k).order_by('-rate')
            mostViewedProducts_total_products = mostViewedProducts.count()
            mostViewedProducts_half_products = math.ceil(mostViewedProducts_total_products/2)
            mostViewedfilterdProducts = []
            count_low,count_up = 0 ,2
            for i in range(0,mostViewedProducts_half_products):
                mostViewedRowProducts = mostViewedProducts[count_low:count_up]
                mostViewedRowProductListWithImage = []
                for j in mostViewedRowProducts:
                    mostViewedRowProductListWithImage.append(productSerialize(j.id)) 
                mostViewedfilterdProducts.append(mostViewedRowProductListWithImage)
                count_low += 2
                count_up += 2
            mostViewedfilterdProductsWithCategorys.append(mostViewedfilterdProducts)

        #Latest Arrivals Section
        latestArrivalsProductsObject = LatestArrivals.objects.get(products_for = 'latestarrivals')
        latestArrivalsProductsInLoop = latestArrivalsProductsObject.products.all()
        latestArrivalsProducts = []
        for i in latestArrivalsProductsInLoop:
            latestArrivalsProducts.append(productSerialize(i.id))

        #Cart Item Section
        delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Dhaka')
        delivery_charge = delivery_charge_object.fee
        price_total = 0
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            cartItems = order.get_cart_items
            cartTotal = order.get_cart_total
            items = order.orderitem_set.all()
            total_items = items.count()
            if total_items> 0:
                for item in items:
                    product = Product.objects.get(id = item.product.id)
                    item.sizes = product.size.all()
                    item.colors = product.color.all()
                    item.image = ProductImages.objects.filter(product = product)[:1]
                    price_total += product.price
            
                total = float(price_total) + float(delivery_charge)
                context = {
                    'mvproducts':mostViewedfilterdProductsWithCategorys,
                    'ltproducts':latestArrivalsProducts,
                    'nvCategorys':navbarCategorys,
                    'mvCategorys':mostViewedCategorys,
                    'items':items,
                    'cartItems':cartItems,
                    'cartTotal':cartTotal,
                    'order':order,
                    'item.image':item.image,
                    'item.sizes':item.sizes,
                    'item.colors':item.colors,
                    'delivery_charge':delivery_charge,
                    'total':total,
                }
            else:
                context = {
                    'mvproducts':mostViewedfilterdProductsWithCategorys,
                    'ltproducts':latestArrivalsProducts,
                    'nvCategorys':navbarCategorys,
                    'mvCategorys':mostViewedCategorys,
                    'cartItems':cartItems,
                }

        else:
            cookieData = cookieCart(request)
            cartItems = cookieData['cartItems']
            cartTotal = cookieData['cartTotal']
            order = cookieData['order']
            items = cookieData['items']
            total_items = len(items)

            if total_items > 0:

                for item in items:
                    product = Product.objects.get(id = item['product']['id'])
                    item['sizes'] = product.size.all()
                    item['colors'] = product.color.all()
                    item['image'] = ProductImages.objects.filter(product = product)[:1]
                    price_total += product.price
            
                total = float(price_total) + float(delivery_charge)
                context = {
                    'mvproducts':mostViewedfilterdProductsWithCategorys,
                    'ltproducts':latestArrivalsProducts,
                    'mvCategorys':mostViewedCategorys,
                    'nvCategorys':navbarCategorys,
                    'items':items,
                    'cartItems':cartItems,
                    'cartTotal':cartTotal,
                    'order':order,
                    'item.image':item['image'],
                    'item.sizes':item['sizes'],
                    'item.colors':item['colors'],
                    'delivery_charge':delivery_charge,
                    'total':total,
                }
            else:
                context = {
                    'mvproducts':mostViewedfilterdProductsWithCategorys,
                    'ltproducts':latestArrivalsProducts,
                    'nvCategorys':navbarCategorys,
                    'mvCategorys':mostViewedCategorys,
                    'cartItems':cartItems,
                }

    else:
        context = {
        }
    return render(request,'store/store.html',context)

def productView(request,pk):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    product = Product.objects.get(id = pk)
    images = ProductImages.objects.filter(product=product)
    big_img = ProductImages.objects.filter(product=product)[:1]
    for i in big_img:
        print(i.Z_img)
    reviews = Review.objects.filter(product=product)
    total_review = reviews.count()
    context = {
        'product':product,
        'nvCategorys':navbarCategorys,
        'images':images,
        'big_img':big_img,
        'reviews':reviews,
        'total_review':total_review
    }

    return render(request,'store/productView.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']
    color = data['color']
    size = data['size']


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(customer=customer, order=order,  product=product)
    if size and color != "undefined":
       orderItem.color = color
       orderItem.size = size

    orderItem.rate = product.price

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    elif action == 'delete':
        orderItem.quantity = 0
    
    elif action == 'color':
        orderItem.color = color
    
    elif action == 'size':
        orderItem.size = size
    
    orderItem.total = (orderItem.quantity * product.price)
            
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        email = request.user.email
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

    else:
        customer,order = guestOrder(request,data)
                
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
        print(order.complete)
        delivery_charge = Delivery_charge.objects.all()
        for i in delivery_charge:
            chrge = i.fee
            discount = i.discount
        
        order.delivery_fee = chrge
        order.total = total + chrge
        order.save()

    return JsonResponse('Order completed!', safe=False)

def cart(request):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()
    
    delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Dhaka')
    delivery_charge = delivery_charge_object.fee
    related_categorys = []
    related_products = []

    # Related products 
    for i in related_categorys:
        products = Product.objects.filter(category = i)
        for j in products:
            related_products.append(productSerialize(j.id))

    if request.user.is_authenticated:
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

        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.cupon_code = cupon
        order.cupon_amount = amount
        order.save()
        cartItems = order.get_cart_items
        cartTotal = order.get_cart_total
        items = order.orderitem_set.all()
        total_items = items.count()
        if total_items> 0:
            for item in items:
                product = Product.objects.get(id = item.product.id)
                categorys = product.category.all()
                for i in categorys:
                    related_categorys.append(i)
                item.sizes = product.size.all()
                item.colors = product.color.all()
                item.image = ProductImages.objects.filter(product = product)[:1]

            total = float(cartTotal) + float(delivery_charge) - float(order.cupon_amount)


            context = {
                'items':items,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
                'nvCategorys':navbarCategorys,
                'order':order,
                'item.image':item.image,
                'item.sizes':item.sizes,
                'item.colors':item.colors,
                'delivery_charge':delivery_charge,
                'total':total,
                'related_products':related_products
            }
           
        else:
            context = {
                'items':items,
                'nvCategorys':navbarCategorys,
                'cartItems':cartItems,
                'order':order,
            }

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        cartTotal = cookieData['cartTotal']
        order = cookieData['order']
        items = cookieData['items']
        total_items = len(items)

        if total_items > 0:

            for item in items:
                product = Product.objects.get(id = item['product']['id'])
                categorys = product.category.all()
                for i in categorys:
                    related_categorys.append(i)
                item['sizes'] = product.size.all()
                item['colors'] = product.color.all()
                item['image'] = ProductImages.objects.filter(product = product)[:1]

            total = float(cartTotal) + float(delivery_charge) - float(order['cupon_amount'])

            context = {
                'items':items,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
                'nvCategorys':navbarCategorys,
                'order':order,
                'item.image':item['image'],
                'item.sizes':item['sizes'],
                'item.colors':item['colors'],
                'delivery_charge':delivery_charge,
                'total':total,
                'related_products':related_products
            }
            
        else:
            context = {
                'items':items,
                'cartItems':cartItems,
                'nvCategorys':navbarCategorys,
                'cartTotal':cartTotal,
                'order':order,
            }
    
    

    return render(request,'store/cart.html',context)


def checkout(request):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()
    
    shipping = None
    delivery_charge = 60
    

    if shipping != None:
        if shipping.city == 'Dhaka':
            delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Dhaka')
            delivery_charge = delivery_charge_object.fee
        else:
            delivery_charge = 120

        
    if request.user.is_authenticated:
        customer = request.user.customer
        shipping = ShippingAddress.objects.get(customer = customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
        cartTotal = order.get_cart_total
        items = order.orderitem_set.all()
        bkash_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order.cupon_amount))
        nagad_total = math.ceil(float(cartTotal) + float(cartTotal * 0.01494) - float(order.cupon_amount))
        if request.method == 'POST' and 'trxid' in request.POST: 
            method = request.POST.get('method')
            trxid = request.POST.get('trxid')
            amount = request.POST.get('amount')
            if method == 'bkash':
                order.total = float(bkash_total) + float(delivery_charge)
            elif method == 'nagad':
                order.total = float(nagad_total) + float(delivery_charge)
            if method == 'cod':
                order.total = float(cartTotal) - float(order.cupon_amount) + float(delivery_charge)
                trxid = 'Cash on delivery'
                amount = 0

            order.transaction_id = trxid
            order.advance = amount
            order.due = float(order.total) - float(order.advance)
            order.save()
        
        if request.method == 'POST' and 'order_confirm' in request.POST: 
            order.status = 'Customer Confirmed'
            order.complete = True
            order.save()
            return redirect('store:home')

        total_items = items.count()
        if total_items> 0:
            for item in items:
                product = Product.objects.get(id = item.product.id)
                item.image = ProductImages.objects.filter(product = product)[:1]
        
        
            context = {
                'items':items,
                'order':order,
                'nvCategorys':navbarCategorys,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
                'shipping':shipping,
                'bkash_total':bkash_total,
                'nagad_total':nagad_total,
                'item.image':item.image,
                'delivery_charge':delivery_charge
            }
        else:
            context = {
                'items':items,
                'order':order,
                'cartItems':cartItems,
                'nvCategorys':navbarCategorys,
                'cartTotal':cartTotal,
                'shipping':shipping,
                'bkash_total':bkash_total,
                'nagad_total':nagad_total,
                'delivery_charge':delivery_charge
            }

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        cartTotal = cookieData['cartTotal']
        order = cookieData['order']
        items = cookieData['items']
        if request.method =='POST' and 'login_username' in request.POST:
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
            if user is not None:
                customer = Customer.objects.get(phone = login_username)
                shipping = ShippingAddress.objects.get(customer = customer)
                db_order, created = Order.objects.get_or_create(customer=customer, complete=False)
                db_order.cupon_code = order['cupon_code']
                db_order.cupon_amount = order['cupon_amount']
                db_order.save()
                shipping.order.add(db_order)
                for item in items:
                    product = Product.objects.get(id=item['product']['id'])
                    quantity = item['quantity']
                    rate = product.price
                    total = float(product.price) * float(quantity)
                    orderItem = OrderItem.objects.get_or_create(
                        product=product,
                        order = db_order,
                        customer=customer, 
                        quantity = item['quantity'],
                        size = item['size'],
                        color = item['color'],
                        rate = rate,
                        total = total
                        )
                login(request,user)

        if request.method =='POST' and 'reg_name' in request.POST:
            name =  request.POST.get('reg_name')
            email =  request.POST.get('reg_email')
            phone =  request.POST.get('reg_phone')
            password1 =  request.POST.get('reg_password1')
            password2 =  request.POST.get('reg_password2')
            address =  request.POST.get('address')
            area =  request.POST.get('area')
            city =  request.POST.get('city')
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken.')
                print("email is taken")
                return redirect('store:checkout')
            elif Customer.objects.filter(phone = phone).first():
                messages.success(request, 'Phone is used on another account.')
                return redirect('store:checkout')
            elif password1 != password2:
                print("password didn't match!")
                messages.success(request, "Password didn't match!.")
                return redirect('store:checkout')
            else:
                user = User.objects.create(first_name = name, email=email,username=phone)
                user.set_password(password1)
                user.save()
                customer = Customer.objects.create(
                        user = user,
                        phone = phone,
                )
                shipping =  ShippingAddress.objects.create(
                    customer = customer,
                    address = address,
                    state = area,
                    city = city
                )
                group = Group.objects.get(name = 'customer')
                user.groups.add(group)
                print("looged in")
                if user is not None:
                    db_order, created = Order.objects.get_or_create(customer=customer, complete=False)
                    shipping.order.add(db_order)
                    for item in items:
                        product = Product.objects.get(id=item['product']['id'])
                        quantity = item['quantity']
                        rate = product.price
                        total = float(product.price) * float(quantity)
                        orderItem = OrderItem.objects.get_or_create(
                            product=product,
                            order = db_order,
                            customer=customer, 
                            quantity = item['quantity'],
                            size = item['size'],
                            color = item['color'],
                            rate = rate,
                            total = total
                            )
                    login(request,user)
        bkash_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order['cupon_amount']))
        nagad_total = math.ceil(float(cartTotal) + float(cartTotal * 0.01494) - float(order['cupon_amount']))
        
        total_items = len(items)
        if total_items> 0:
            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                item['image'] = ProductImages.objects.filter(product = product)[:1]
        

            context = {
                'items':items,
                'order':order,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
                'shipping':shipping,
                'nvCategorys':navbarCategorys,
                'bkash_total':bkash_total,
                'nagad_total':nagad_total,
                'item.image':item['image'],
                'delivery_charge':delivery_charge
            }
        else:
            context = {
                'items':items,
                'order':order,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
                'nvCategorys':navbarCategorys,
                'shipping':shipping,
                'bkash_total':bkash_total,
                'nagad_total':nagad_total,
                'delivery_charge':delivery_charge
            }
    return render(request,'store/checkout.html',context)

def categoryView(request,pk):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    #Neccesary items
    start_price = 200
    end_price = 3000
    sort_name = 'default'
    necessaryItems = {
        'sort_details': sort_name,
        'pricedetails':{
            'start_price': start_price,
            'end_price' : end_price
        },
    }
    
    #Category Section
    selectedCategory = Category.objects.get(id=pk)
    products = Product.objects.filter(category = selectedCategory)
    if request.method == 'POST' and 'sort-details' in request.POST:
        sort_details = request.POST.get('sort-details')
        necessaryItems['sort_details'] = sort_details
        if sort_details == 'default':
            products = products
        elif sort_details == 'name_a_z':
            products = Product.objects.filter(category = selectedCategory).order_by('name')
        elif sort_details == 'name_z_a':
            products = Product.objects.filter(category = selectedCategory).order_by('-name')
        elif sort_details == 'price_l_h':
            products = Product.objects.filter(category = selectedCategory).order_by('price')
        elif sort_details == 'price_h_l':
            products = Product.objects.filter(category = selectedCategory).order_by('-price')
        elif sort_details == 'rate_h_l':
            products = Product.objects.filter(category = selectedCategory).order_by('-rate')
        elif sort_details == 'rate_l_h':
            products = Product.objects.filter(category = selectedCategory).order_by('rate')
            
        start_price =  request.POST.get('start_price')
        end_price =  request.POST.get('end_price')
        priceProducts = products.filter(category = selectedCategory , price__gte =  start_price, price__lte = end_price)
        products = priceProducts
        necessaryItems['pricedetails']['start_price'] = start_price
        necessaryItems['pricedetails']['end_price'] = end_price

    categoryWithDetailedProduct = []
    allCategorys = Category.objects.all()
    for i in allCategorys:
        categoryWithDetailedProduct.append(category_with_products(i.id))

    outputProduct = []
    for k in products:
        outputProduct.append(productSerialize(k.id))
    
    context = {
        'nvCategorys':navbarCategorys,
        'selectedCategory':selectedCategory,
        'categoryWithDetailedProduct':categoryWithDetailedProduct,
        'necessaryItems':necessaryItems,
        'products':outputProduct,
    }
    return render(request,'store/categoryView.html',context)

def searchProduct(request,*arg,**kwargs):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    #Neccesary items
    start_price = 200
    end_price = 3000
    sort_name = 'default'
    necessaryItems = {
        'sort_details': sort_name,
        'pricedetails':{
            'start_price': start_price,
            'end_price' : end_price
        },
    }

    query = kwargs.pop('searchtext')
    products = Product.objects.filter(Q(name__icontains=query))
    

    if request.method == 'POST' and 'search' in request.POST:
        queryText = request.POST.get('search')
        category_id = request.POST.get('category_id')
        description = request.POST.get('description')

        if description is None:
            c_products = Product.objects.filter(category = category_id)
            products = c_products.filter(Q(name__icontains=queryText))
        else:
            c_products = Product.objects.filter(category = category_id)
            products = c_products.filter(Q(name__icontains=queryText) | Q(description__icontains=queryText))
    
    if request.method == 'POST' and 'sort-details' in request.POST:
        sort_details = request.POST.get('sort-details')
        necessaryItems['sort_details'] = sort_details
        if sort_details == 'default':
            products = products
        elif sort_details == 'name_a_z':
            products = products.order_by('name')
        elif sort_details == 'name_z_a':
            products = products.order_by('-name')
        elif sort_details == 'price_l_h':
            products = products.order_by('price')
        elif sort_details == 'price_h_l':
            products = products.order_by('-price')
        elif sort_details == 'rate_h_l':
            products = products.order_by('-rate')
        elif sort_details == 'rate_l_h':
            products = products.order_by('rate')
            
        start_price =  request.POST.get('start_price')
        end_price =  request.POST.get('end_price')
        priceProducts = products.filter(price__gte =  start_price, price__lte = end_price)
        products = priceProducts
        necessaryItems['pricedetails']['start_price'] = start_price
        necessaryItems['pricedetails']['end_price'] = end_price


    outputProduct = []
    for k in products:
        outputProduct.append(productSerialize(k.id))

    categorys = Category.objects.all()

    context ={
        'nvCategorys':navbarCategorys,
        'products':outputProduct,
        'searchText':query,
        'categorys':categorys,
        'necessaryItems':necessaryItems,

    }
    return render(request,'store/searchProduct.html',context)