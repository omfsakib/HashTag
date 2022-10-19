from django.contrib import admin
from .models import *

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone","date_created")
    search_fields = ("phone", )  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","price","get_category")
    list_filter = ("category",)
    search_fields = ("name", )

    def get_category(self, obj):
        return "\n".join([p.name for p in obj.category.all()])


admin.site.register(Order)
admin.site.register(Delivery_charge)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Cupon)
admin.site.register(Review)
admin.site.register(ProductImages)
admin.site.register(ShippingAddress)
admin.site.register(IndivitualCategory)
admin.site.register(LatestArrivals)

admin.site.site_header = "HashTag Admin Panel"
admin.site.site_title = "HashTag Admin Portal"
admin.site.index_title = "Welcome to HashTag Portal"