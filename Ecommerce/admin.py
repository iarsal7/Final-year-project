from django.contrib import admin
from .models import Category , Product ,Tag, Cart, Order, OrderDetail ,User , Review
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin 
from .models import User
# from .forms import MyUserCreationForm, MyUserChangeForm

class MyUserAdmin(UserAdmin):
    # add_form = MyUserCreationForm
    # form = MyUserChangeForm
    model = User
    list_display = ['username','email', 'first_name','last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('address','phone')}),
    ) 

admin.site.register(User ,MyUserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(Review)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('number','user__username' )
    list_display = ['number' , 'user','user_address','date','time','shippingtotal','total' ,'status']

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['orderid' , 'productname','quantity','total']
