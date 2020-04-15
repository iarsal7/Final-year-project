from django.contrib import admin
from .models import Category , Product , Customer
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)

