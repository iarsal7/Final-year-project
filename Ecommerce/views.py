from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect , JsonResponse
from django.views.generic import ListView,View,CreateView
from .forms import  SearchForm ,MyUserCreationForm
from .models import Product , Category, Cart , Order ,OrderDetail ,User,Review , ProductImage , Review , Variation , ItemVariation , Variant, Wishlist , Subcategory
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
from django.db.models import Case, When
import random


def home(request):

    realme= Subcategory.objects.get(name='Realme')
    products= Product.objects.filter(category=realme)      
    
    #Featured
    featured= Product.objects.filter(featured=True)

    queryset = Product.objects.all()
    
    
    sale=queryset.random(16)  # pass amount to get more records


    rated= Product.objects.all().order_by('rating')[:16]  

    new= Product.objects.all().order_by('-id')[:20]

    category= Category.objects.get(name='Laptops')
    laptops= Product.objects.filter(category__category= category)

    vid=  Category.objects.filter( Q(name='DSLR Canon Cameras') | Q(name='DSLR Nikon Cameras') | Q(name='Audio/Video Cameras')  )
    
  
    video= Product.objects.filter(category__category__in = vid).distinct()
    
    iphone= Product.objects.get(id=23)

    context={

        "deal":products, "featured":featured, "sale":sale , "rated":rated , "new":new , "video":video , "laptops":laptops , "iphone":iphone

           }
    return render(request, 'home.html',context)

class SignUpView(CreateView):
    form_class = MyUserCreationForm
    success_url = 'login'
    template_name = 'signup.html'

def productList(request):

    product = Product.objects.all()

    return render(request , 'productList.html' , {'product':product })
    


def productDetails(request , id):
    
    try:
        product = Product.objects.get(id=id)
        photos = ProductImage.objects.filter(product=product)


    except Product.DoesNotExist: 
        raise Http404('product not found') 

    user= User.objects.filter(username=request.user).first()

    #wishlist
    wishlist= Wishlist.objects.filter(products=product , user=user).first()
     
    # Size Variation    

    variation = Variation.objects.filter(product=product)
    size = variation.first()
    size_variation= ItemVariation.objects.filter(variation= size)
     
    # Variants
    variants=[]
    variant = Variant.objects.filter(product= product).first()
    if variant is not None:
        variant_id= variant.variant_key
        variants= Variant.objects.filter(variant_key= variant_id).exclude(product=product)
    
    review_list = Review.objects.filter(product=product , user=user , status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(review_list, 5)
    
    try:
        review = paginator.page(page)
    except PageNotAnInteger:
        review = paginator.page(1)
    except EmptyPage:
        review= paginator.page(paginator.num_pages)
    
    queryset = get_recommendations(product.id)
    
    context={
        'product':product , 'photos':photos , 'review':review , 'size':size , 'size_variation':size_variation,
            'variants':variants , 'wishlist':wishlist , 'recommendation': queryset
    }

    return render(request , 'productDetails.html' , context)

def featuredList(request):

    product = Product.objects.filter(featured=True)

    return render(request , 'featuredList.html' , {'product':product})

def featuredDetails(request , id):
    try:
        product = Product.objects.get(id=id , featured=True)
      

    except Product.DoesNotExist: 
        raise Http404('product not found')

    return render(request , 'featuredDetails.html' , {'product':product})

            
def searchproduct(request):
    if request.method == 'GET':
        search= request.GET.get('q')
        submit= request.GET.get('submit')
        if search is not None:
            query= Q(title__icontains=search) | Q(description__icontains=search) | Q(tag__name__icontains=search)
            products= Product.objects.filter(query).distinct()

            context={'products': products,
                     'submit': submit}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')

@login_required
def cart(request):
    cart_obj=request.user.carts.all()
    Gtotal=0
    for cart_total in cart_obj:
        Gtotal+= cart_total.total
    
    if request.method=='POST':
        product_id= request.POST.get('product_id')
        quantity= request.POST.get('quantity')
        size= request.POST.get('size_mark')
        print(size)
        product=Product.objects.get(id=product_id)
        cart= Cart.objects.filter(user=request.user , products=product, note=size).first()
        if cart is not None:
            cart.note=size
            qnty= cart.quantity + int(quantity)
            total= qnty * product.price
            cart.quantity += int(quantity)
            cart.total=total
            cart.save()
        else:
            cart_obj= Cart.objects.create(user= request.user)
            cart_obj.products=product
            cart_obj.quantity=quantity
            total=Decimal(cart_obj.quantity) * product.price
            cart_obj.total= total
            cart_obj.note=size
            cart_obj.save()

            request.session['item_count'] = request.user.carts.all().count() #Counting items for navbar

            if request.is_ajax():
                data={

                    "cartCount":request.user.carts.all().count(),
                    "Gtotal": Gtotal
                }    
                return JsonResponse(data)
        
    return render(request, 'cart.html' ,{'cart':cart_obj ,'Gtotal':Gtotal})

class cartupdate(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        print(id1)
        quantity= request.GET.get('quantity', None)
        size= request.GET.get('size', None)
        print("arsal")
        print(size)
        product=Product.objects.get(id=id1)
        cart=Cart.objects.filter(user=request.user , products=product , note=size).first()
        cart.quantity=quantity
        cart.total=Decimal(quantity) * product.price
        cart.save()
        total= cart.total
        cart_obj=request.user.carts.all()
        Gtotal=0
        for cart_total in cart_obj:
            Gtotal+= cart_total.total

        carttable= {'status': 'ok',
           "Gtotal": Gtotal,
           'total' : total,
           'quantity':quantity,
           'id': id1,
           'name': product.title
           
           }
        data = {
            'cart': carttable
        }

        return JsonResponse(data)

class cartdelete(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        size= request.GET.get('size', None)
        print("arsal")
        print(size)
        product=Product.objects.get(id=id1)
        cart=Cart.objects.filter(user=request.user , products=product , note=size)
        cart.delete()
        cart_obj=request.user.carts.all()
        Gtotal=0
        for cart_total in cart_obj:
            Gtotal+= cart_total.total
        data = {
            'deleted': True,
            "cartCount":request.user.carts.all().count(),
             "Gtotal": Gtotal
        }
        return JsonResponse(data)

class cartlogin(View):
    def  get(self, request):
        username = request.GET.get('username', None)
        password=  request.GET.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'login failed'})

def checkout(request):
    cart_obj=Cart.objects.filter(user=request.user)
    total=0
    for cart_total in cart_obj:
        total+= cart_total.total
    total= int(total)
    shipping=120

    gtotal= total + shipping

    user= User.objects.get(username=request.user)
    context={
        "cart":cart_obj,
        "user":user,
        "total":total,
        "shipping":shipping,
        "Gtotal":gtotal
    }
    return render(request , 'checkout.html', context)


class updateUser(View):
    def  get(self, request):
        print("in update user")
        fname = request.GET.get('fname', None)
        lname=  request.GET.get('lname', None)
        phone=  request.GET.get('phone', None)
        email=  request.GET.get('email', None)
        address=  request.GET.get('address', None)

        user= User.objects.get(username=request.user)
        user.first_name= fname
        user.last_name= lname
        user.phone= phone
        user.email=email
        user.address=address
        user.save()
        return JsonResponse({'status': 'updated'})

class order(View):
    def  get(self, request):
        order_obj= Order.objects.create(user= request.user)
        shipping=120
        order_obj.shippingtotal=shipping
        total=0
        cart_obj=Cart.objects.filter(user=request.user)
        for cart_total in cart_obj:
            total+= cart_total.total
        total=int(total)+shipping
        order_obj.total= total
        order_obj.save()

        for obj in cart_obj:
            order_detail= OrderDetail.objects.create(orderid=order_obj ,products=obj.products)
            order_detail.products=obj.products
            order_detail.productname= obj.products.title
            order_detail.quantity=obj.quantity
            order_detail.total=obj.total
            order_detail.note=obj.note        
            order_detail.save()

        cart_obj.delete()

        return JsonResponse({'status': 'ok'})   

def success(request):

    return render(request , 'success.html', {})



class review(View):
    def  get(self, request):
        productid=request.GET.get('id', None) 
        subject = request.GET.get('subject', None)
        comment=  request.GET.get('comment', None)
        rating=  request.GET.get('rating', None)
        
        product=Product.objects.get(id= productid)
        review_obj= Review.objects.create(user=request.user , product=product)
        review_obj.subject=subject
        review_obj.comment=comment
        review_obj.rating= rating
        review_obj.save()
        total = 0
        for obj in product.reviews.all():
            total += obj.rating
        
        count= product.reviews.all().count()
        total = total/count

        product.rating= total
        product.save()

        messages.success(request, 'Form submission successful')
        return JsonResponse({'status': 'ok'})


def test(request):

    context={
       
    }

    return render(request , 'test.html' ,context)

def loginSignup(request):

    return render(request , 'login-signup.html' ,{})

class loginUser(View):
    def  get(self, request):
        username = request.GET.get('username', None)
        password=  request.GET.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'login failed'})

def profile(request):
    user= User.objects.filter(username=request.user).first()
    order= Order.objects.filter(user=user).order_by('-date', '-time')
    
    return render(request , 'userprofile.html' , { 'order': order })

def orderdetails(request , id):
    
    orderdetail= OrderDetail.objects.filter(orderid__number=id)
    
    return render(request , 'orderdetails.html', {'orderdetail': orderdetail , 'number':id})


class updateWishlist(View):

    def  get(self, request):
        productid=request.GET.get('id', None)

        product= Product.objects.get(id= productid)

        wish= Wishlist.objects.filter(user=request.user , products=product).first()
        
        if wish is not None:
            wish.save()


        else:

            wishlist= Wishlist.objects.create(products=product , user= request.user)

            wishlist.save()

        data={
                    "wishCount":request.user.wishlists.all().count(),
                }    


        return JsonResponse(data)

class removeWishlist(View):

    def get(self, request):
    
        productid=request.GET.get('id', None)

        product= Product.objects.get(id= productid)

        wish= Wishlist.objects.filter(user=request.user , products=product).first()

        if wish is not None:
            wish.delete()

        data={
            'deleted': True,
            "wishCount":request.user.wishlists.all().count(),
                    }    

        return JsonResponse(data)

def wishlist(request):

    user= User.objects.filter(username=request.user).first()
    wishlist= Wishlist.objects.filter(user=user)

    return render(request , 'wishlist.html' ,{'wishlist':wishlist})

def get_recommendations(productid):
    product_list=[]
    product=Product.objects.get(id=productid)
    variant = Variant.objects.filter(product= product).first()
    if variant is not None:
        variant_id= variant.variant_key
        variants= Variant.objects.filter(variant_key= variant_id).exclude(product=product)
        
        for obj in variants:
            product_list.append(obj.product.id)

    product_list.append(productid)
    orders = pd.DataFrame(list(OrderDetail.objects.filter().values('orderid__number' , 'products__id')))
    orders_for_product = orders[orders.products__id.isin(product_list)].orderid__number.unique()
    relevant_orders = orders[orders.orderid__number.isin(orders_for_product)]
    accompanying_products_by_order = relevant_orders[~relevant_orders.products__id.isin(product_list)]
    num_instance_by_accompanying_product = accompanying_products_by_order.groupby("products__id")["products__id"].count().reset_index(name="instances")
    num_orders_for_product = orders_for_product.size
    product_instances = pd.DataFrame(num_instance_by_accompanying_product)
    product_instances["frequency"] = product_instances["instances"]/num_orders_for_product
    recommended_products = pd.DataFrame(product_instances.sort_values("frequency", ascending=False).head(5))
    product = recommended_products['products__id'].values.tolist()
    queryset = Product.objects.filter(pk__in=product)
    print(queryset)

    return queryset


def shop(request ,pk):
    
    x= pk.replace('-', ' ')
    category= Subcategory.objects.get(name=x)
    products= Product.objects.filter(category=category)
    return render(request , 'shop.html' , {'products':products , 'category':x})

def smartphones(request , pk):

    x= pk.replace('-', ' ')
    category= Category.objects.get(name= x)
    products= Product.objects.filter(category__category= category)
    return render(request , 'smartphones.html' , {'products':products , 'category':category})
