from multiprocessing import context
from unicodedata import category
from django.shortcuts import render
from .models import *
from .utils import *
import math
from django.http import JsonResponse
import datetime

# Create your views here.
def home(request):
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
                    'mvCategorys':mostViewedCategorys,
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
                    'mvCategorys':mostViewedCategorys,
                    'cartItems':cartItems,
                }

    else:
        context = {
        }
    return render(request,'store/store.html',context)

def productView(request,pk):
    product = Product.objects.get(id = pk)
    images = ProductImages.objects.filter(product=product)
    big_img = ProductImages.objects.filter(product=product)[:1]
    for i in big_img:
        print(i.Z_img)
    reviews = Review.objects.filter(product=product)
    total_review = reviews.count()
    context = {
        'product':product,
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

    orderItem, created = OrderItem.objects.get_or_create(customer=customer, order=order,  product=product, status='Pending')
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
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
        )
        
    return JsonResponse('Order completed!', safe=False)

def cart(request):
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
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
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

            total = float(cartTotal) + float(delivery_charge) - float(order['cupon_amount'])


            context = {
                'items':items,
                'cartItems':cartItems,
                'cartTotal':cartTotal,
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
                'cartTotal':cartTotal,
                'order':order,
            }
    
    

    return render(request,'store/cart.html',context)