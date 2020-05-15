from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect , JsonResponse
from django.views.generic import ListView,View,CreateView
from .forms import  SearchForm ,MyUserCreationForm
from .models import Product , Cart , Order ,OrderDetail ,User,Review , ProductImage , Review , Variation , ItemVariation
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    
    products = Product.objects.all()
    
    context={

        "products":products
    }
    return render(request, 'home.html',context)

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST or None)
#         Customer_Form = CustomerForm(request.POST or None)
#         if form.is_valid() and Customer_Form.is_valid():
#             user = form.save()
#             customer= Customer_Form.save(commit=False)
#             customer.user=user
#             customer.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = SignUpForm()
#         Customer_Form = CustomerForm()
        
#     return render(request, 'signup.html', {'form': form , 'Cform' : Customer_Form})

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


    variation = Variation.objects.filter(product=product)
    size = variation.first()
    size_variation= ItemVariation.objects.filter(variation= size)
     

    
    review_list = Review.objects.filter(product=product , user=request.user , status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(review_list, 5)
    
    try:
        review = paginator.page(page)
    except PageNotAnInteger:
        review = paginator.page(1)
    except EmptyPage:
        review= paginator.page(paginator.num_pages)

    context={
        'product':product , 'photos':photos , 'review':review , 'size':size , 'size_variation':size_variation,
    
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
        size= request.POST.get('size')
        print(size)
        quantity= request.POST.get('quantity')
        product=Product.objects.get(id=product_id)
        cart= Cart.objects.filter(user=request.user , products=product).first()
        if cart is not None:
            cart.quantity += int(quantity)
            cart.save()
        else:
            cart_obj= Cart.objects.create(user= request.user)
            cart_obj.products=product
            cart_obj.quantity=quantity
            total=Decimal(cart_obj.quantity) * product.price
            cart_obj.total= total
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
        quantity= request.GET.get('quantity', None)
        product=Product.objects.get(id=id1)
        cart=Cart.objects.get(user=request.user , products=product)
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
        product=Product.objects.get(id=id1)
        cart=Cart.objects.filter(user=request.user , products=product)
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
        messages.success(request, 'Form submission successful')
        return JsonResponse({'status': 'ok'})
        
def test(request):
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
