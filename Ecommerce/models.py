from django.db import models
import random , os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    

class Customer(models.Model):
    user= models.OneToOneField(User , on_delete=models.CASCADE )
    address= models.TextField()
    phone = models.CharField(max_length=11)


