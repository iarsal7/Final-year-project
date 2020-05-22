from django.contrib import admin
from .models import Category , Product ,Tag, Cart, Order, OrderDetail ,User , Review, Variant , ProductImage, Subcategory , Variation , ItemVariation , Wishlist
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
admin.site.register(Subcategory)


admin.site.register(Cart)
admin.site.register(Wishlist)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin,]
    search_fields = ('id','title' )
    list_display = ['id','title' ,'description']
    
    class Meta:
       model = Product

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]    

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
    
class ItemVariationAdmin(admin.StackedInline):
    model = ItemVariation


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    inlines = [ItemVariationAdmin]
    list_display = ['product' ,'name']
    
    class Meta:
       model = Variation

@admin.register(ItemVariation)
class ItemVariationAdmin(admin.ModelAdmin):
    list_display=['variation' , 'value']




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('number','user__username' )
    list_display = ['number' , 'user','user_address','date','time','shippingtotal','total' ,'status']

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['orderid' , 'productname', 'note', 'quantity','total']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product' , 'user','subject','comment' ,'rating', 'date' ,'time']

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['variant_key' , 'product_key' , 'product']

