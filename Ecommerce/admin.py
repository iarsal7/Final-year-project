from django.contrib import admin
from .models import Category , Product , Customer ,Tag, Cart, Order, OrderDetail
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Cart)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number' , 'user','date','time','shippingtotal','total']

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['orderid' , 'productname','quantity','total']
