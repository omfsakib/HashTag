from multiprocessing import context
from unicodedata import category
from django.shortcuts import render
from .models import *
from .utils import *
import math

# Create your views here.
def home(request):
    total_products = Product.objects.all().count()

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
    
        
    if total_products > 0: 
        context = {
            'mvproducts':mostViewedfilterdProductsWithCategorys,
            'mvCategorys':mostViewedCategorys,
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