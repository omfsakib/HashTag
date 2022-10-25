from django.contrib.auth.hashers import check_password
from django.urls import reverse
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
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    #CartItem Section
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    cartTotal = cookieData['cartTotal']
    order = cookieData['order']
    items = cookieData['items']
    total_items = len(items)
    delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Dhaka')
    delivery_charge = delivery_charge_object.fee
    price_total = 0

    #Login Section
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
            db_order.address = shipping.address
            db_order.city = shipping.city
            db_order.state = shipping.state
            db_order.save()
            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                quantity = item['quantity']
                rate = product.price
                total = float(product.price) * float(quantity)
                orderItem, created  = OrderItem.objects.get_or_create(
                    product=product,
                    order = db_order,
                    customer=customer
                )
                orderItem.quantity=item['quantity']
                orderItem.size = item['size']
                orderItem.color = item['color']
                orderItem.rate = rate,
                orderItem.total = total
                orderItem.save()
            login(request,user)
            messages.success(request,'Login Successfull!')
            return redirect('store:home')
        else:
            messages.error(request,'Login failed. Please try again!')
            return redirect('store:login')
    if total_items > 0:
        for item in items:
            product = Product.objects.get(id = item['product']['id'])
            item['sizes'] = product.size.all()
            item['colors'] = product.color.all()
            item['image'] = ProductImages.objects.filter(product = product)[:1]
            price_total += product.price
    
        total = float(price_total) + float(delivery_charge)

        context ={
            'cartItems':cartItems,
            'cartTotal':cartTotal,
            'nvCategorys':navbarCategorys,
            'order':order,
            'items':items,
            'item.image':item['image'],
            'item.sizes':item['sizes'],
            'item.colors':item['colors'],
            'delivery_charge':delivery_charge,
            'total':total,

        }
    else:
        context ={
            'cartItems':cartItems,
            'cartTotal':cartTotal,
            'nvCategorys':navbarCategorys,

        }
    return render(request,'accounts/login.html',context)

def signUpUser(request):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    #CartItem Section
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    cartTotal = cookieData['cartTotal']
    order = cookieData['order']
    items = cookieData['items']
    total_items = len(items)
    delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Dhaka')
    delivery_charge = delivery_charge_object.fee
    price_total = 0

    #SignUp Section
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
            messages.error(request, 'Email is taken.')
            return redirect('store:sign_up')
        elif Customer.objects.filter(phone = phone).first():
            messages.error(request, 'Phone is used on another account.')
            return redirect('store:sign_up')
        elif password1 != password2:
            messages.error(request, "Password didn't match!.")
            return redirect('store:sign_up')
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
            if user is not None:
                db_order, created = Order.objects.get_or_create(customer=customer, complete=False)
                db_order.address = shipping.address
                db_order.city = shipping.city
                db_order.state = shipping.state
                db_order.save()
                for item in items:
                    product = Product.objects.get(id=item['product']['id'])
                    quantity = item['quantity']
                    rate = product.price
                    total = float(product.price) * float(quantity)
                    orderItem, created  = OrderItem.objects.get_or_create(
                       product=product,
                        order = db_order,
                        customer=customer, 
                        )
                    orderItem.quantity=item['quantity']
                    orderItem.size = item['size']
                    orderItem.color = item['color']
                    orderItem.rate = rate,
                    orderItem.total = total
                    orderItem.save()
                login(request,user)
            messages.success(request,'Login Successfull!')
        return redirect('store:home')
    
    if total_items > 0:
        for item in items:
            product = Product.objects.get(id = item['product']['id'])
            item['sizes'] = product.size.all()
            item['colors'] = product.color.all()
            item['image'] = ProductImages.objects.filter(product = product)[:1]
            price_total += product.price
    
        total = float(price_total) + float(delivery_charge)

        context ={
            'cartItems':cartItems,
            'cartTotal':cartTotal,
            'nvCategorys':navbarCategorys,
            'order':order,
            'items':items,
            'item.image':item['image'],
            'item.sizes':item['sizes'],
            'item.colors':item['colors'],
            'delivery_charge':delivery_charge,
            'total':total,

        }
    else:
        context ={
            'cartItems':cartItems,
            'cartTotal':cartTotal,
            'nvCategorys':navbarCategorys,

        }
    return render(request,'accounts/registration.html',context)

def accountProfile(request,pk):
    user = request.user
    customer = request.user.customer
    user_orders = Order.objects.filter(customer=customer,complete = True).order_by('-date_created')

    #Status Section 
    total_orders = user_orders.count()
    delivered = user_orders.filter(status = 'Delivered').count()
    transit = user_orders.filter(status = 'In-Transit').count()
    confirmed = user_orders.filter(status = 'Admin Confirmed').count()
    pending = user_orders.filter(status = 'Customer Confirmed').count()
    
    status = {
        'total_orders':total_orders,
        'delivered':delivered,
        'transit':transit,
        'confirmed':confirmed, 
        'pending':pending,
    }

    #Shipping Section
    shipping = ShippingAddress.objects.get(customer = customer)

    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    #Account Edit Section
    if request.method == 'POST'and 'account_name' in request.POST:
        account_name = request.POST.get('account_name')
        account_email = request.POST.get('account_email')
        account_telephone = request.POST.get('account_telephone')
        account_image = request.FILES.get('account_image')
        user.first_name = account_name
        user.email = account_email
        if User.objects.filter(username = account_telephone).exclude(username = user.username).exists():
            messages.error(request,'Account exists with this phone number!')
            return redirect(reverse('store:account_profile', kwargs={'pk':pk}))
        elif Customer.objects.filter(phone = account_telephone).exclude(phone = customer.phone).exists():
            messages.error(request,'Account exists with this phone number!')
            return redirect(reverse('store:account_profile', kwargs={'pk':pk}))
        else:
            user.username = account_telephone

        user.save()
        if account_image is not None:
            customer.phone = account_telephone
            customer.profile_pic = account_image
        else:
            customer.phone = account_telephone
        customer.save()
        messages.success(request,'Information updated!')
        return redirect(reverse('store:account_profile', kwargs={'pk':pk}))

    if request.method == 'POST' and 'old_password' in request.POST:
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password1')
        if check_password(old_password,user.password):
            if new_password1 != new_password2:
                messages.error(request,"Password didn't match. Please enter it again.")
            elif new_password1 == old_password:
                messages.error(request,"New password can't be as same as old password.")
            else:
                user.set_password(new_password1)
                user.save()
                login(request,user)
                messages.success(request,'Password updated!')
        else:
            messages.error(request,'Your old password was entered incorrectly. Please enter it again.')

        return redirect(reverse('store:account_profile', kwargs={'pk':pk}))
    
    if request.method == 'POST' and 'address' in request.POST:
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        shipping.address = address
        shipping.state = state
        shipping.city = city
        shipping.save()
        messages.success(request,'Billing details updated!')
        return redirect(reverse('store:account_profile', kwargs={'pk':pk}))

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
                'status':status,
                'filterOrders':user_orders,
                'nvCategorys':navbarCategorys,
                'shipping':shipping,
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
                'status':status,
                'filterOrders':user_orders,
                'nvCategorys':navbarCategorys,
                'shipping':shipping,
                'cartItems':cartItems,
            }
    return render(request,'accounts/accountProfile.html',context)

def home(request):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    #Member Discount
    if request.method == 'POST' and 'subscribe_email' in request.POST:
        subscribe_email = request.POST.get('subscribe_email')
        if Subscription.objects.filter(email= subscribe_email).exists():
            messages.error(request,'This email already subscribed!')
            return redirect('store:home')
        else:
            Subscription.objects.create(email = subscribe_email)
            messages.success(request,'Subscription successfull!')
            return redirect('store:home')



    total_products = Product.objects.all().count()
    if total_products > 0:

        #Home Banner Section
        homeBannerCategoryWithImage = HomeBannerCategory.objects.all()[:3]

        #Collection Category Section
        collectionCategoryWithImage = CollectionCategory.objects.all()[:3]

        #ShopNow Category Section
        shopNowCategoryWithImage = ShopNowCategorys.objects.all()[:2]

        #Blog Section
        blogs = []
        tmp_blogs = Blog.objects.all().order_by('-date_added')
        for i in tmp_blogs:
            blogs.append(blogs_with_detailed_date(i.id))

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
                    'blogs':blogs,
                    'sncimage':shopNowCategoryWithImage,
                    'ccimage':collectionCategoryWithImage,
                    'hbcimage':homeBannerCategoryWithImage,
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
                    'blogs':blogs,
                    'sncimage':shopNowCategoryWithImage,
                    'ccimage':collectionCategoryWithImage,
                    'hbcimage':homeBannerCategoryWithImage,
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
                    'blogs':blogs,
                    'sncimage':shopNowCategoryWithImage,
                    'ccimage':collectionCategoryWithImage,
                    'hbcimage':homeBannerCategoryWithImage,
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
                    'blogs':blogs,
                    'sncimage':shopNowCategoryWithImage,
                    'ccimage':collectionCategoryWithImage,
                    'hbcimage':homeBannerCategoryWithImage,
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

    #Review Section
    reviews = []
    tmp_reviews = Review.objects.filter(product=product)
    total_review = tmp_reviews.count()
    review_count = 0
    for i in tmp_reviews:
        reviews.append(reviews_with_images(i.id))
        review_count += i.rate
        product.rate = float(review_count/total_review)
        product.save()

    if request.method == 'POST':
        comment = request.POST.get('review_comment')
        rate = request.POST.get('review_rate')
        review_images = request.FILES.getlist('review_images')
        new_review = Review.objects.create(user = request.user.customer, product = product)
        new_review.comment = comment
        new_review.rate = rate
        new_review.save()
        for i in review_images:
            new_image = ReviewImages.objects.create(review = new_review,img = i)
        return redirect(reverse('store:product_view', kwargs={'pk':pk}))

    #Releted Product Section
    categorys = product.category.all()
    reletedProducts = []
    for i in categorys:
        category_product = Product.objects.filter(category=i).order_by('-rate')
        for j in category_product:
            reletedProducts.append(productSerialize(j.id))

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
                'product':product,
                'nvCategorys':navbarCategorys,
                'images':images,
                'big_img':big_img,
                'reviews':reviews,
                'total_review':total_review,
                'items':items,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
                'order':order,
                'item.image':item.image,
                'item.sizes':item.sizes,
                'item.colors':item.colors,
                'delivery_charge':delivery_charge,
                'total':total,
                'rltdProducts':reletedProducts,
            }
        else:
            context = {
                'product':product,
                'nvCategorys':navbarCategorys,
                'images':images,
                'big_img':big_img,
                'reviews':reviews,
                'total_review':total_review,
                'cartItems':cartItems,
                'rltdProducts':reletedProducts,
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
                'product':product,
                'nvCategorys':navbarCategorys,
                'images':images,
                'big_img':big_img,
                'reviews':reviews,
                'total_review':total_review,
                'items':items,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
                'order':order,
                'item.image':item['image'],
                'item.sizes':item['sizes'],
                'item.colors':item['colors'],
                'delivery_charge':delivery_charge,
                'total':total,
                'rltdProducts':reletedProducts,
            }
        else:
            context = {
                'product':product,
                'nvCategorys':navbarCategorys,
                'images':images,
                'big_img':big_img,
                'reviews':reviews,
                'total_review':total_review,
                'cartItems':cartItems,
                'rltdProducts':reletedProducts,
            }

    return render(request,'store/productView.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']
    color = data['color']
    size = data['size']
    quantity = data['quantity']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(customer=customer, order=order,  product=product)
    if size and color != "undefined":
       orderItem.color = color
       orderItem.size = size

    if quantity == 'undefined':
        quantity = 1

    orderItem.rate = product.price

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + int(quantity))

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


def cart(request):
    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

    #Member Discount
    if request.method == 'POST' and 'subscribe_email' in request.POST:
        subscribe_email = request.POST.get('subscribe_email')
        if Subscription.objects.filter(email= subscribe_email).exists():
            messages.error(request,'This email already subscribed!')
            return redirect('store:cart')
        else:
            Subscription.objects.create(email = subscribe_email)
            messages.success(request,'Subscription successfull!')
            return redirect('store:cart')
    
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
    
    member = False
    percentageAmount = 0
    

    if shipping != None:
        if shipping.city == 'Dhaka':
            delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Dhaka')
            delivery_charge = delivery_charge_object.fee
        else:
            delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Other')
            delivery_charge = delivery_charge_object.fee

        
    if request.user.is_authenticated:
        
        customer = request.user.customer
        shipping = ShippingAddress.objects.get(customer = customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        if Order.objects.filter(customer=customer,complete=True,cupon_code = order.cupon_code).exists():
            order.cupon_code += '- expired'
            order.cupon_amount = 0
            order.save()
        cartItems = order.get_cart_items
        cartTotal = order.get_cart_total
        if Subscription.objects.filter(email = request.user.email).exists():
            member = True
            if cartTotal >= 2000 :
                percentageAmount = float(cartTotal) * 0.05

        items = order.orderitem_set.all()
        bkash_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order.cupon_amount) - float(percentageAmount)) 
        nagad_total = math.ceil(float(cartTotal) + float(cartTotal * 0.01494) - float(order.cupon_amount) - float(percentageAmount)) 
        if request.method == 'POST' and 'trxid' in request.POST: 
            method = request.POST.get('method')
            trxid = request.POST.get('trxid')
            amount = request.POST.get('amount')
            if method == 'bkash':
                order.method = 'bkash'
                order.total = float(bkash_total) + float(delivery_charge)
            elif method == 'nagad':
                order.method = 'nagad'
                order.total = float(nagad_total) + float(delivery_charge)
            if method == 'cod':
                order.method = 'cod'
                order.total = float(cartTotal) - float(order.cupon_amount) + float(delivery_charge) - float(percentageAmount)
                trxid = 'Cash on delivery'
                amount = 0


            order.transaction_id = trxid
            order.advance = amount
            order.due = float(order.total) - float(order.advance)
            order.save()
            return redirect('store:checkout')
        
        if request.method == 'POST' and 'order_confirm' in request.POST: 
            order.status = 'Customer Confirmed'
            order.address = shipping.address
            order.city = shipping.city
            order.member_amount = percentageAmount
            order.state = shipping.state
            order.delivery_fee = delivery_charge
            order.complete = True
            order.save()
            return redirect('store:home')

        total_items = items.count()
        if total_items> 0:
            for item in items:
                product = Product.objects.get(id = item.product.id)
                item.image = ProductImages.objects.filter(product = product)[:1]
        
            
            context = {
                'member':member,
                'percentageAmount':percentageAmount,
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
                'percentageAmount':percentageAmount,
                'member':member,
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
                db_order.address = shipping.address
                db_order.city = shipping.city
                db_order.state = shipping.state
                db_order.save()
                for item in items:
                    product = Product.objects.get(id=item['product']['id'])
                    quantity = item['quantity']
                    rate = product.price
                    total = float(product.price) * float(quantity)
                    orderItem, created  = OrderItem.objects.get_or_create(
                        product=product,
                        order = db_order,
                        customer=customer, 
                        )
                    orderItem.quantity=item['quantity']
                    orderItem.size = item['size']
                    orderItem.color = item['color']
                    orderItem.rate = rate
                    orderItem.total = total
                    orderItem.save()
                login(request,user)
                
            messages.success(request,'Login Successfull!')

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
                messages.error(request, 'Email is taken.')
                return redirect('store:checkout')
            elif Customer.objects.filter(phone = phone).first():
                messages.error(request, 'Phone is used on another account.')
                return redirect('store:checkout')
            elif password1 != password2:
                messages.error(request, "Password didn't match!.")
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
                if user is not None:
                    db_order, created = Order.objects.get_or_create(customer=customer, complete=False)
                    db_order.address = shipping.address
                    db_order.state = shipping.state
                    db_order.city = shipping.city
                    db_order.save()
                    for item in items:
                        product = Product.objects.get(id=item['product']['id'])
                        quantity = item['quantity']
                        rate = product.price
                        total = float(product.price) * float(quantity)
                        orderItem, created  = OrderItem.objects.get_or_create(
                            product=product,
                            order = db_order,
                            customer=customer
                        )
                        orderItem.quantity=item['quantity']
                        orderItem.size = item['size']
                        orderItem.color = item['color']
                        orderItem.rate = rate
                        orderItem.total = total
                        orderItem.save()
                    login(request,user)
                    
            messages.success(request,'SignuP Successfull!')
        bkash_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order['cupon_amount']))
        nagad_total = math.ceil(float(cartTotal) + float(cartTotal * 0.01494) - float(order['cupon_amount']))
        
        total_items = len(items)
        if total_items> 0:
            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                item['image'] = ProductImages.objects.filter(product = product)[:1]
        

            context = {
                'percentageAmount':percentageAmount,
                'member':member,
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
                'percentageAmount':percentageAmount,
                'member':member,
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
                'nvCategorys':navbarCategorys,
                'selectedCategory':selectedCategory,
                'categoryWithDetailedProduct':categoryWithDetailedProduct,
                'necessaryItems':necessaryItems,
                'products':outputProduct,
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
                'nvCategorys':navbarCategorys,
                'selectedCategory':selectedCategory,
                'categoryWithDetailedProduct':categoryWithDetailedProduct,
                'necessaryItems':necessaryItems,
                'products':outputProduct,
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
                'nvCategorys':navbarCategorys,
                'selectedCategory':selectedCategory,
                'categoryWithDetailedProduct':categoryWithDetailedProduct,
                'necessaryItems':necessaryItems,
                'products':outputProduct,
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
                'nvCategorys':navbarCategorys,
                'selectedCategory':selectedCategory,
                'categoryWithDetailedProduct':categoryWithDetailedProduct,
                'necessaryItems':necessaryItems,
                'products':outputProduct,
                'cartItems':cartItems,
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
                'nvCategorys':navbarCategorys,
                'products':outputProduct,
                'searchText':query,
                'categorys':categorys,
                'necessaryItems':necessaryItems,
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
                'nvCategorys':navbarCategorys,
                'products':outputProduct,
                'searchText':query,
                'categorys':categorys,
                'necessaryItems':necessaryItems,
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
                
                'nvCategorys':navbarCategorys,
                'products':outputProduct,
                'searchText':query,
                'categorys':categorys,
                'necessaryItems':necessaryItems,
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
                'nvCategorys':navbarCategorys,
                'products':outputProduct,
                'searchText':query,
                'categorys':categorys,
                'necessaryItems':necessaryItems,
                'cartItems':cartItems,
            }

    return render(request,'store/searchProduct.html',context)

def blog(request,pk):
    blog = blogs_with_detailed_date(pk)

    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

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
                'blog':blog,
                'nvCategorys':navbarCategorys,
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
                'blog':blog,
                'nvCategorys':navbarCategorys,
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
                
                'blog':blog,
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
                'blog':blog,
                'nvCategorys':navbarCategorys,
                'cartItems':cartItems,
            }
    return render(request,'store/blog.html',context)

def blogs(request):
    #Blogs Section
    blogs = []
    tmp_blogs = Blog.objects.all().order_by('-date_added')
    for i in tmp_blogs:
        blogs.append(blogs_with_detailed_date(i.id))

    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

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
                'blogs':blogs,
                'nvCategorys':navbarCategorys,
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
                'blogs':blogs,
                'nvCategorys':navbarCategorys,
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
                
                'blogs':blogs,
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
                'blogs':blogs,
                'nvCategorys':navbarCategorys,
                'cartItems':cartItems,
            }
    return render(request,'store/blogs.html',context)

def view_order(request,pk):
    user_order = Order.objects.get(id = pk)
    user_order_items = OrderItem.objects.filter(order=user_order)

    #Navbar Section
    navbarCategoryObject =  IndivitualCategory.objects.get(category_for = 'navbar')
    navbarCategorys = navbarCategoryObject.categorys.all()

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
                'viewOrder': user_order,
                'viewItems': user_order_items,
                'viewNeed':order_with_discount_details(pk),
                'nvCategorys':navbarCategorys,
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
                'viewOrder': user_order,
                'viewItems': user_order_items,
                'viewNeed':order_with_discount_details(pk),
                'nvCategorys':navbarCategorys,
                'cartItems':cartItems,
            }
    return render(request,'store/viewOrder.html',context)