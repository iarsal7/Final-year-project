from django.db import models
import random , os
from django.contrib.auth.models import User
from django.db.models.signals import post_save , pre_save , m2m_changed
from django.dispatch import receiver
from Ecommerce.utils import unique_order_id_generator

def upload_image_to(instance , filename): #For Creating New Filename
    new_filename = random.randint(1 , 3456423)
    base_name = os.path.basename(filename)
    name , ext = os.path.splitext(base_name)
    name = new_filename
    return "{name}{ext}".format(name=name , ext=ext)
    
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = ('category')
        verbose_name_plural = ('categories')

    def __str__(self):
        return self.name
        

class Product(models.Model):
    title= models.CharField(max_length=120)
    description=models.TextField()
    category = models.ForeignKey(Category , on_delete= models.CASCADE , related_name='products')
    price=models.DecimalField(decimal_places=2 , max_digits=20)
    image=models.ImageField(upload_to=upload_image_to)
    featured=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name= models.CharField(max_length=100)
    product= models.ManyToManyField(Product)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user= models.OneToOneField(User , on_delete=models.CASCADE)
    address= models.TextField()
    phone = models.CharField(max_length=11)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    products= models.ForeignKey(Product , on_delete=models.Case, related_name='carts' ,null=True , blank=True)
    quantity= models.IntegerField(null=True , blank=True)
    total= models.DecimalField(decimal_places=2 , max_digits=100 ,null=True ,blank=True)

    def __str__(self):
        return str(self.id)



class Order(models.Model):
    number= models.CharField(max_length=100 , blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date= models.DateField(auto_now_add=True, auto_now=False)
    time=models.TimeField(auto_now_add=True , auto_now=False)
    shippingtotal= models.DecimalField(decimal_places=2 , max_digits=100 ,null=True ,blank=True)
    total = models.DecimalField(decimal_places=2 , max_digits=100 ,null=True ,blank=True)


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
        return str(self.id)
