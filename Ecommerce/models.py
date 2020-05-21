from django.db import models
import random , os
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save , pre_save , m2m_changed
from django.dispatch import receiver
from Ecommerce.utils import unique_order_id_generator

class User(AbstractUser):
    address= models.TextField(blank=True)
    phone = models.CharField(max_length=11 , blank=True)


def upload_image_to(instance , filename): #For Creating New Filename
    new_filename = random.randint(1 , 3456423)
    base_name = os.path.basename(filename)
    name , ext = os.path.splitext(base_name)
    name = new_filename
    return "{name}{ext}".format(name=name , ext=ext)
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = ('category')
        verbose_name_plural = ('categories')

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name

        

class Product(models.Model):
    title= models.CharField(max_length=120)
    description=models.TextField()
    category = models.ForeignKey(Subcategory , on_delete= models.CASCADE , related_name='products')
    price=models.DecimalField(decimal_places=2 , max_digits=20)
    image=models.ImageField(upload_to=upload_image_to)
    featured=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " " + self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='productimages') 
    images = models.FileField(upload_to = upload_image_to)

    def __str__(self):
        return self.product.title
    

class Variant(models.Model):
    class Meta:
        unique_together = (('variant_key', 'product_key'),)

    variant_key = models.IntegerField(null=True , blank=True)
    product_key = models.IntegerField(null=True , blank=True)
    product= models.ForeignKey(Product , on_delete=models.CASCADE)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='variations')
    name= models.CharField(max_length=50)

    class Meta:
        unique_together = (('product', 'name'),)

    def __str__(self):
        return self.name
    
    

class ItemVariation(models.Model):
    variation= models.ForeignKey(Variation , on_delete= models.CASCADE ,related_name='itemvariations')
    value= models.CharField(max_length=50)  
    
    class Meta:
        unique_together = (('variation', 'value'),)


class Review(models.Model):
    status=models.BooleanField(default=False)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='reviews')
    user= models.ForeignKey(User , on_delete=models.CASCADE , related_name='reviews')
    subject= models.CharField(max_length=50)
    comment= models.CharField(max_length=250)
    rating= models.IntegerField(null=True , blank=True)
    date= models.DateField(auto_now_add=True, auto_now=False)
    time=models.TimeField(auto_now_add=True , auto_now=False)

    

class Tag(models.Model):
    name= models.CharField(max_length=100)
    product= models.ManyToManyField(Product)

    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    products= models.ForeignKey(Product , on_delete=models.Case, related_name='carts' ,null=True , blank=True)
    quantity= models.IntegerField(null=True , blank=True)
    note= models.TextField(blank=True , null=True)
    total= models.DecimalField(decimal_places=2 , max_digits=100 ,null=True ,blank=True)

    def __str__(self):
        return str(self.id)

order_choices=(            
    ('created','Created'),
    ('shipped','Shipped'),
    ('refunded','Refunded')
)

class Order(models.Model):
    number= models.CharField(max_length=100 , blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date= models.DateField(auto_now_add=True, auto_now=False)
    time=models.TimeField(auto_now_add=True , auto_now=False)
    shippingtotal= models.DecimalField(decimal_places=2 , max_digits=100 ,null=True ,blank=True)
    total = models.DecimalField(decimal_places=2 , max_digits=100 ,null=True ,blank=True)
    status= models.CharField(max_length=120 , default='created' , choices=order_choices )

    def user_address(self):
        return self.user.address

    def __str__(self):
        return self.number


def pre_save_order_number(sender, instance , *args, **kwargs):
    if not instance.number:
        instance.number= unique_order_id_generator(instance)
pre_save.connect(pre_save_order_number, sender=Order)

class OrderDetail(models.Model):
    orderid= models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderDetails')
    products= models.ForeignKey(Product, on_delete=models.CASCADE , related_name='orderDetails')
    productname=models.CharField(max_length=120)
    quantity= models.IntegerField(null=True , blank=True)
    total = models.DecimalField(decimal_places=2 , max_digits=100 ,null=True ,blank=True)

    def __str__(self):
        return str(self.orderid)
    


class Wishlist(models.Model):
    products= models.ForeignKey(Product, on_delete=models.CASCADE , related_name='wishlists')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')