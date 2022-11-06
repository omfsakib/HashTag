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
from .forms import *
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

@login_required(login_url='store:login')
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

    #Wish List Section
    wish_products = []
    total_wish_products = 0
    if WishList.objects.filter(customer = customer).exists():
        wish_object = WishList.objects.get(customer = customer)
        for i in wish_object.products.all():
            wish_products.append(productSerialize(i.id))
        total_wish_products = wish_object.products.all().count()

    wish_list = {
        'total_products': total_wish_products,
        'wish_products':wish_products,
    }
    if request.method == 'POST' and 'remove_wish' in request.POST:
        remove_wish = request.POST.get('remove_wish')
        wish_remove_product = Product.objects.get(id = remove_wish)
        wish_remove_object = WishList.objects.get(customer = request.user.customer)
        wish_remove_object.products.remove(wish_remove_product)
        messages.success(request,'Product successfully removed from wish list!')
        return redirect(reverse('store:account_profile', kwargs={'pk':pk}))

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
                'wish_list':wish_list,
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
                'wish_list':wish_list,
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

    #WishList Section
    if request.user.is_authenticated:
        wish_customer = request.user.customer
        if request.method == 'POST' and 'wish-List' in request.POST:
            wish_product = request.POST.get('wish-List')
            if WishList.objects.filter(customer = wish_customer).exists():
                wish_object = WishList.objects.get(customer = wish_customer)
            else:
                wish_object = WishList.objects.create(customer = wish_customer)
            wish_object.products.add(wish_product)
            wish_object.save()
            messages.success(request,'Product added to Wish List!')
            return redirect(reverse('store:product_view', kwargs={'pk':pk}))

            

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

    if request.method == 'POST' and 'review_comment' in request.POST:
        comment = request.POST.get('review_comment')
        rate = request.POST.get('review_rate')
        review_images = request.FILES.getlist('review_images')
        new_review = Review.objects.create(user = request.user.customer, product = product)
        new_review.comment = comment
        new_review.rate = rate
        new_review.save()
        for i in review_images:
            new_image = ReviewImages.objects.create(review = new_review,img = i)
        
        messages.success(request,'Review added successfully!')
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

    delivery_charge = 60
    
    shipping = None
    member = False
    percentageAmount = 0
    
        
    if request.user.is_authenticated:
        
        customer = request.user.customer
        shipping = ShippingAddress.objects.get(customer = customer)
        if shipping.city == 'Dhaka':
            delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Dhaka')
            delivery_charge = delivery_charge_object.fee

        else:
            delivery_charge_object = Delivery_charge.objects.get(w_delivery= 'Other')
            delivery_charge = delivery_charge_object.fee

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
                percentageAmount = math.floor(float(cartTotal) * 0.05)

        items = order.orderitem_set.all()
        bkash_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order.cupon_amount) - float(percentageAmount) + float(delivery_charge)) 
        nagad_total = math.ceil(float(cartTotal) + float(cartTotal * 0.01494) - float(order.cupon_amount) - float(percentageAmount) + float(delivery_charge)) 
        rocket_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order.cupon_amount) - float(percentageAmount) + float(delivery_charge)) 
        if request.method == 'POST' and 'method' in request.POST: 
            method = request.POST.get('method')
            if method == 'bkash':
                order.method = 'bkash'
                order.total = float(bkash_total)
            elif method == 'nagad':
                order.method = 'nagad'
                order.total = float(nagad_total) 
            elif method == 'rocket':
                order.method = 'rocket'
                order.total = float(rocket_total) 
            if method == 'cod':
                order.method = 'cod'
                order.total = float(cartTotal) - float(order.cupon_amount) + float(delivery_charge) - float(percentageAmount)


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
            messages.success(request,'Order completed! you can track order from dashboard!')
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
                'rocket_total':rocket_total,
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
                'rocket_total':rocket_total,
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
                db_order,created = Order.objects.get_or_create(customer=customer, complete=False)
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
                return redirect('store:checkout')
                
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
                    db_order,created = Order.objects.get_or_create(customer=customer, complete=False)
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
                    return redirect('store:checkout')
                    
            messages.success(request,'SignuP Successfull!')
        bkash_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order['cupon_amount']))
        nagad_total = math.ceil(float(cartTotal) + float(cartTotal * 0.01494) - float(order['cupon_amount']))
        rocket_total = math.ceil(float(cartTotal) + float(cartTotal * 0.02) - float(order['cupon_amount'])) 
        
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
                'rocket_total':rocket_total,
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
                'rocket_total':rocket_total,
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


@login_required(login_url='store:login')
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


class shopDashboard(View):

    def get(self,request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            orders = []
            tmp_orders = Order.objects.filter(complete = True).order_by('-date_created')
            
            #Status Section 
            total_orders = tmp_orders.count()
            delivered = tmp_orders.filter(status = 'Delivered').count()
            transit = tmp_orders.filter(status = 'In-Transit').count()
            confirmed = tmp_orders.filter(status = 'Admin Confirmed').count()
            pending = tmp_orders.filter(status = 'Customer Confirmed').count()
            returns = tmp_orders.filter(status = 'Return').count()
            cancel = tmp_orders.filter(status = 'Cancel').count()

            status = {
                'total_orders':total_orders,
                'delivered':delivered,
                'transit':transit,
                'confirmed':confirmed, 
                'pending':pending,
                'return':returns,
                'cancel':cancel
            }

            for i in tmp_orders:
                orders.append(orderFetch(i.id))
            return JsonResponse({'orders':orders,'status':status})
        context = {}
        return render(request,'shop/pages/shopDashboard.html',context)


def updateOrder(request,pk):
    user_order = Order.objects.get(id = pk)
    user_order_items = OrderItem.objects.filter(order=user_order)
    if request.method ==  'POST' and 'status' in request.POST:
        status = request.POST.get('status')
        user_order.status = status
        user_order.save()
        messages.success(request,'Status updated!')
        return redirect(reverse('store:update-order', kwargs={'pk':pk}))

    if request.method ==  'POST' and 'amount' in request.POST:
        amount = request.POST.get('amount')
        user_order.advance += float(amount)
        user_order.due = float(user_order.total) - float(user_order.advance)
        user_order.save()
        messages.success(request,'Amount added!')
        return redirect(reverse('store:update-order', kwargs={'pk':pk}))

    context = {
        'viewOrder': user_order,
        'viewItems': user_order_items,
        'viewNeed':order_with_discount_details(pk),
        }
    return render(request,'shop/pages/updateOrder.html',context)

def products(request):
    products = []
    tmp_products = Product.objects.all().order_by('-date_created')
    for i in tmp_products:
        products.append(productSerialize(i.id))

    product_categorys = Category.objects.all().order_by('name')
    product_sizes = Size.objects.all().order_by('size')
    product_colors = Color.objects.all().order_by('color')

    #Add Product Section
    if request.method == 'POST' and 'product_name' in request.POST:
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        code = request.POST.get('product_code')
        stock = request.POST.get('product_stock')
        description = request.POST.get('product_description')
        categorys = request.POST.getlist('product_categorys')
        sizes = request.POST.getlist('product_sizes')
        colors = request.POST.getlist('product_colors')
        image = request.FILES.get('product_image')
        zoom_image = request.FILES.get('product_image2')
        new_product = Product.objects.create(
            name = name,
            price = price,
            product_code = code,
            stock = stock,
            description = description,
        )
        for category in categorys:
            new_product.category.add(category)
        
        for size in sizes:
            new_product.size.add(size)
        
        for color in colors:
            new_product.color.add(color)

        prodduct_img = ProductImages.objects.create(
            product = new_product,
            n_img = image,
            Z_img = zoom_image
        )
        messages.success(request,'Product added successfully!')
        return redirect('store:products')
    
    #Delete Product Section
    if request.method == 'POST' and 'product_delete' in request.POST:
        id = request.POST.get('product_delete')
        delete_product = Product.objects.get(id = id)
        images_of_delete_products = ProductImages.objects.filter(product = delete_product)
        for i in images_of_delete_products:
            i.delete()
        delete_product.delete()
        messages.success(request,'Product deleted successfully!')
        return redirect('store:products')

    #Add Category Section
    if request.method == 'POST' and 'category_name' in request.POST:
        category_name = request.POST.get('category_name')
        new_category = Category.objects.create(name=category_name)
        messages.success(request,'Category added successfully!')
        return redirect('store:products')
    
    #Delete Category Section
    if request.method == 'POST' and 'category_delete' in request.POST:
        id = request.POST.get('category_delete')
        delete_category = Category.objects.get(id = id)
        delete_category.delete()
        messages.success(request,'Category deleted successfully!')
        return redirect('store:products')
    
     #Add Color Section
    if request.method == 'POST' and 'color_name' in request.POST:
        color_name = request.POST.get('color_name')
        new_color = Color.objects.create(color=color_name)
        messages.success(request,'Color added successfully!')
        return redirect('store:products')
    
    #Delete Color Section
    if request.method == 'POST' and 'color_delete' in request.POST:
        id = request.POST.get('color_delete')
        delete_color = Color.objects.get(id = id)
        delete_color.delete()
        messages.success(request,'Color deleted successfully!')
        return redirect('store:products')

    #Add Size Section
    if request.method == 'POST' and 'size_name' in request.POST:
        size_name = request.POST.get('size_name')
        new_size = Size.objects.create(size=size_name)
        messages.success(request,'Size added successfully!')
        return redirect('store:products')
    
    #Delete Size Section
    if request.method == 'POST' and 'size_delete' in request.POST:
        id = request.POST.get('size_delete')
        delete_size = Size.objects.get(id = id)
        delete_size.delete()
        messages.success(request,'Size deleted successfully!')
        return redirect('store:products')

    context = {
        'products':products,
        'categorys':product_categorys,
        'sizes':product_sizes,
        'colors':product_colors,
    }
    return render(request,'shop/pages/products.html',context)

def shopProductView(request,pk):
    #Product Section
    product = Product.objects.get(id=pk)
    images = ProductImages.objects.filter(product=product)
    big_img = ProductImages.objects.filter(product=product)[:1]
    product_categorys = Category.objects.all().order_by('name')
    product_sizes = Size.objects.all().order_by('size')
    product_colors = Color.objects.all().order_by('color')

    #Update Product Section
    form = ProductForm(instance=product)
    if request.method == "POST" and 'name' in request.POST:
        stock = request.POST.get('edit_product_stock')
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            product.stock += int(stock)
            product.save()
            messages.success(request,'Product updated successfully!')
            return redirect(reverse('store:shop_product_view', kwargs={'pk':pk}))
        else:
            print(form.errors)
            form = ProductForm(instance=product)
    
    #Delete Product Section
    if request.method == 'POST' and 'product_delete' in request.POST:
        id = request.POST.get('product_delete')
        delete_product = Product.objects.get(id = id)
        images_of_delete_products = ProductImages.objects.filter(product = delete_product)
        for i in images_of_delete_products:
            i.delete()
        delete_product.delete()
        messages.success(request,'Product deleted successfully!')
        return redirect(reverse('store:shop_product_view', kwargs={'pk':pk}))
    
    #Delete Review Section
    if request.method == 'POST' and 'review_delete' in request.POST:
        id = request.POST.get('review_delete')
        delete_review = Review.objects.get(id = id)
        images_of_delete_review = ReviewImages.objects.filter(review = delete_review)
        for i in images_of_delete_review:
            i.delete()
        delete_review.delete()
        messages.success(request,'Review deleted successfully!')
        return redirect(reverse('store:shop_product_view', kwargs={'pk':pk}))

    #Upload Image Section
    if request.method == 'POST' and 'product_id' in request.POST:
        product_id = request.POST.get('product_id')
        image = request.FILES.get('product_image')
        zoom_image = request.FILES.get('product_image2')
        print(product_id)
        img_product = Product.objects.get(id = product_id)
        new_images = ProductImages.objects.create(product = img_product)
        new_images.n_img = image
        new_images.Z_img = zoom_image
        new_images.save()
        messages.success(request,'Image added successfully!')
        return redirect(reverse('store:shop_product_view', kwargs={'pk':pk}))

    #Delete Image Section
    if request.method == 'POST' and 'image_delete' in request.POST:
        id = request.POST.get('image_delete')
        delete_image = ProductImages.objects.get(id = id)
        delete_image.delete()
        messages.success(request,'Image deleted successfully!')
        return redirect(reverse('store:shop_product_view', kwargs={'pk':pk}))

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

    

    context={
        'product':product,
        'images':images,
        'big_img':big_img,
        'total_review':total_review,
        'reviews':reviews,
        'categorys':product_categorys,
        'sizes':product_sizes,
        'colors':product_colors,
        'form':form
    }
    return render(request,'shop/pages/productView.html',context)


def storeSettings(request):
    #Neccesary Items
    categorys = Category.objects.all()

    #Banner Section
    homebannerItems = HomeBannerCategory.objects.all()[:3]
    total_home_banner_items = homebannerItems.count()

    #Upload Home Banner
    if request.method == 'POST' and 'title_heading' in request.POST:
        title_heading = request.POST.get('title_heading')
        sub_title_heading = request.POST.get('sub_title_heading')
        short_description = request.POST.get('short_description')
        estimated_category = request.POST.get('estimated_category')
        banner_img = request.FILES.get('banner_img')
        added_category = Category.objects.get(id = estimated_category)
        if HomeBannerCategory.objects.filter(estimated_category = added_category).exists():
            messages.error(request,'Category already in use!')
            return redirect('store:store_setting')
        else:
            new_home_banner =  HomeBannerCategory.objects.create(estimated_category = added_category)
            new_home_banner.title_heading = title_heading
            new_home_banner.sub_title_heading = sub_title_heading
            new_home_banner.short_description = short_description
            new_home_banner.banner_img = banner_img
            new_home_banner.save()
            messages.success(request,'Banner created successfully!')
            return redirect('store:store_setting')

    #Update Home Banner
    if request.method == "POST" and 'banner_id' in request.POST:
        banner_id = request.POST.get('banner_id')
        update_banner_title = request.POST.get('update_banner_title')
        update_banner_subheading = request.POST.get('update_banner_subheading')
        update_short_description = request.POST.get('update_short_description')
        update_estimated_category = request.POST.get('update_estimated_category')
        update_banner_img = request.FILES.get('update_banner_img')
        update_home_banner_object = HomeBannerCategory.objects.get(id = banner_id)
        update_home_banner_object.title_heading = update_banner_title
        update_home_banner_object.sub_title_heading = update_banner_subheading
        update_home_banner_object.short_description = update_short_description
        update_new_category = Category.objects.get(id = update_estimated_category)
        update_home_banner_object.estimated_category = update_new_category
        if update_banner_img:
            update_home_banner_object.banner_img = update_banner_img
        update_home_banner_object.save()
        messages.success(request,'Banner updated successfully!')
        return redirect('store:store_setting')
    
    #Delete Home Banner
    if request.method == 'POST' and 'home_banner_delete' in request.POST:
        id =  request.POST.get('home_banner_delete')
        delete_banner_object =  HomeBannerCategory.objects.get(id = id)
        delete_banner_object.delete()
        messages.success(request,'Banner deleted successfully!')
        return redirect('store:store_setting')

    #Collection 
    collectionItems = CollectionCategory.objects.all()[:3]
    total_collection_items = collectionItems.count()

    #Upload Collection
    if request.method == 'POST' and 'heading' in request.POST:
        heading = request.POST.get('heading')
        sub_heading = request.POST.get('sub_heading')
        up_estimated_category = request.POST.get('estimated_category')
        img = request.FILES.get('img')
        added_category = Category.objects.get(id = up_estimated_category)
        if CollectionCategory.objects.filter(estimated_category = added_category).exists():
            messages.error(request,'Category already in use!')
            return redirect('store:store_setting')
        else:
            new_collection =  CollectionCategory.objects.create(estimated_category = added_category)
            new_collection.heading = heading
            new_collection.sub_heading = sub_heading
            new_collection.img = img
            new_collection.save()
            messages.success(request,'Collection created successfully!')
            return redirect('store:store_setting')

    #Update Collection
    if request.method == 'POST' and 'collection_id' in request.POST:
        collection_id = request.POST.get('collection_id')
        update_collection_title = request.POST.get('update_collection_title')
        update_collection_subheading = request.POST.get('update_collection_subheading')
        update_collection_estimated_category = request.POST.get('update_collection_estimated_category')
        update_collection_img = request.FILES.get('update_collection_img')
        update_collection_object = CollectionCategory.objects.get(id = collection_id)
        update_collection_object.heading  = update_collection_title
        update_collection_object.sub_heading = update_collection_subheading
        update_new_category_collection = Category.objects.get(id = update_collection_estimated_category)
        update_collection_object.estimated_category = update_new_category_collection
        if update_collection_img:
            update_collection_object.img
        update_collection_object.save()

        messages.success(request,'Collection updated successfully!')
        return redirect('store:store_setting')
    
    
    #Delete Collection
    if request.method == 'POST' and 'collection_delete' in request.POST:
        id =  request.POST.get('collection_delete')
        delete_collection_object =  CollectionCategory.objects.get(id = id)
        delete_collection_object.delete()
        messages.success(request,'Collection deleted successfully!')
        return redirect('store:store_setting')

    #ShopNow Category
    shopnowItems = ShopNowCategorys.objects.all()[:2]
    total_shopnow_items = shopnowItems.count()

    #Upload ShopNow Category
    if request.method == 'POST' and 'category_for' in request.POST:
        title = request.POST.get('title')
        sub_title = request.POST.get('sub_title')
        category_for = request.POST.get('category_for')
        sn_estimated_category = request.POST.get('estimated_category')
        up_img = request.FILES.get('img')
        added_category = Category.objects.get(id = sn_estimated_category)
        if ShopNowCategorys.objects.filter(estimated_category = added_category).exists():
            messages.error(request,'Category already in use!')
            return redirect('store:store_setting')
        else:
            new_shopnow =  ShopNowCategorys.objects.create(estimated_category = added_category)
            new_shopnow.title = title
            new_shopnow.sub_title = sub_title
            new_shopnow.category_for = category_for
            new_shopnow.img = up_img
            new_shopnow.save()
            messages.success(request,'Banner created successfully!')
            return redirect('store:store_setting')

     #Update ShopNow Category
    if request.method == 'POST' and 'shopnow_id' in request.POST:
        shopnow_id = request.POST.get('shopnow_id')
        update_shopnow_title = request.POST.get('update_shopnow_title')
        update_shopnow_subheading = request.POST.get('update_shopnow_subheading')
        update_shopnow_category_for = request.POST.get('update_shopnow_category_for')
        update_shopnow_estimated_category = request.POST.get('update_shopnow_estimated_category')
        update_shopnow_img = request.FILES.get('update_shopnow_img')
        update_shopnow_object = ShopNowCategorys.objects.get(id = shopnow_id)
        update_shopnow_object.title  = update_shopnow_title
        update_shopnow_object.sub_title = update_shopnow_subheading
        update_shopnow_object.category_for = update_shopnow_category_for
        update_new_category_shopnow = Category.objects.get(id = update_shopnow_estimated_category)
        update_shopnow_object.estimated_category = update_new_category_shopnow
        if update_shopnow_img:
            update_shopnow_object.img
        update_shopnow_object.save()

        messages.success(request,'Shop Now Category updated successfully!')
        return redirect('store:store_setting')

    #Delete ShopNow Category
    if request.method == 'POST' and 'shopnow_delete' in request.POST:
        id =  request.POST.get('shopnow_delete')
        delete_shopnow_object =  ShopNowCategorys.objects.get(id = id)
        delete_shopnow_object.delete()
        messages.success(request,'Shop Now Category deleted successfully!')
        return redirect('store:store_setting')

    
    #Latest Arrivals
    ltproducts = []
    lt_object =  LatestArrivals.objects.get(products_for = 'latestarrivals')
    for i in lt_object.products.all():
        ltproducts.append(productSerialize(i.id))
    
    products = []
    tmp_products = Product.objects.all().order_by('-date_created')
    for i in tmp_products:
        if i in lt_object.products.all():
            pass
        else:
            products.append(productSerialize(i.id))
    
    #Add Products To Latest Arrivals
    if request.method == 'POST' and 'products_id_list' in request.POST:
        products_id_list = request.POST.getlist('products_id_list')
        for i in products_id_list:
            add_product = Product.objects.get(id = i)
            lt_object.products.add(add_product)

        messages.success(request,'Product added to latest arrivals!')
        return redirect('store:store_setting')

    #Remove Products From Latest Arrivals
    if request.method == 'POST' and 'latest_delete' in request.POST:
        id =  request.POST.get('latest_delete')
        remove_product = Product.objects.get(id = id)
        lt_object.products.remove(remove_product)
        messages.success(request,'Product removed from latest arrivals!')
        return redirect('store:store_setting')

    
    #Indivitual Category Section
    nvCategorys = IndivitualCategory.objects.get(category_for = 'navbar')
    total_nvCategorys = nvCategorys.categorys.all().count()
    mvCategorys = IndivitualCategory.objects.get(category_for = 'mvcategory')
    total_mvCategorys = mvCategorys.categorys.all().count()

    #Add Category
    if request.method == 'POST' and 'category_id_list' in request.POST:
        add_category_for_indivitual = request.POST.get('add_category_for_indivitual')
        category_id_list = request.POST.getlist('category_id_list')
        add_category_for = IndivitualCategory.objects.get(category_for = add_category_for_indivitual)
        for i in category_id_list:
            to_be_add_category = Category.objects.get(id = i)
            add_category_for.categorys.add(to_be_add_category)

        messages.success(request,'Categorys added to indivitual categorys!')
        return redirect('store:store_setting')

    #Remove Category
    if request.method == 'POST' and 'category_for_indivitual' in request.POST:
        category_for_indivitual = request.POST.get('category_for_indivitual')
        category_remove = request.POST.get('category_remove')
        remove_category = Category.objects.get(id = category_remove)
        remove_category_indivitual = IndivitualCategory.objects.get(category_for = category_for_indivitual)
        remove_category_indivitual.categorys.remove(remove_category)
        messages.success(request,'Category removed from indivitual categorys!')
        return redirect('store:store_setting')


    context = {
        'homebannerItems':homebannerItems,
        'total_home_banner_items':total_home_banner_items,
        'collectionItems':collectionItems,
        'total_collection_items':total_collection_items,
        'shopnowItems':shopnowItems,
        'total_shopnow_items':total_shopnow_items,
        'ltproducts':ltproducts,
        'products':products,
        'categorys':categorys,
        'nvCategorys':nvCategorys,
        'total_nvCategorys':total_nvCategorys,
        'mvCategorys':mvCategorys,
        'total_mvCategorys':total_mvCategorys
    }
    return render(request,'shop/pages/storeSetting.html',context)



def bannerSetting(request,pk):
    banner = HomeBannerCategory.objects.get(id = pk)
    category_id = banner.estimated_category.id
    category_name = banner.estimated_category.name

    context = {
        'id':banner.id,
        'title_heading':banner.title_heading,
        'sub_title_heading':banner.sub_title_heading,
        'short_description':banner.short_description,
        'category_id' :category_id,
        'estimated_category':category_name,
        'banner_img':banner.banner_img.url
    }
    return JsonResponse({'banner':context})

def collectionSetting(request,pk):
    collection = CollectionCategory.objects.get(id = pk)
    category_id = collection.estimated_category.id
    category_name = collection.estimated_category.name

    context = {
        'id':collection.id,
        'heading':collection.heading,
        'sub_heading':collection.sub_heading,
        'category_id' :category_id,
        'estimated_category':category_name,
        'img':collection.img.url
    }
    return JsonResponse({'collection':context})

def shopnowSetting(request,pk):
    shopnow = ShopNowCategorys.objects.get(id = pk)
    category_id = shopnow.estimated_category.id
    category_name = shopnow.estimated_category.name

    context = {
        'id':shopnow.id,
        'heading':shopnow.title,
        'sub_heading':shopnow.sub_title,
        'category_for':shopnow.category_for,
        'category_id' :category_id,
        'estimated_category':category_name,
        'img':shopnow.img.url
    }
    return JsonResponse({'shopnow':context})