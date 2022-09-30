from django.shortcuts import render
from .models import *
from .utils import *
import math

# Create your views here.
def home(request):
    total_products = Product.objects.all().count()

    # Most Viewed Section
    mostViewedProducts = Product.objects.all()
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
    

    if total_products > 0: 
        context = {
            'mvproducts':mostViewedfilterdProducts,
        }
    else:
        context = {
        }
    return render(request,'store/store.html',context)