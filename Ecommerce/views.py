from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect , JsonResponse
from django.views.generic import ListView,View,CreateView
from .forms import  SearchForm ,MyUserCreationForm
from .models import Product , Cart , Order ,OrderDetail ,User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.urls import reverse_lazy

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
      

    except Product.DoesNotExist: 
        raise Http404('product not found') 

    return render(request , 'productDetails.html' , {'product':product})

def featuredList(request):

    product = Product.objects.filter(featured=True)

    return render(request , 'featuredList.html' , {'product':product})

def featuredDetails(request , id):
    try:
        product = Product.objects.get(id=id , featured=True)
      

    except Product.DoesNotExist: 
        raise Http404('product not found')

    return render(request , 'featuredDetails.html' , {'product':product})

class SearchProduct(ListView):
    template_name= 'search.html'
    model=Product
    messages='No Result Found'
    def get_queryset(self):
        query= self.request.GET.get('q', None)
        if query:
            search= Q(title__icontains=query) | Q(description__icontains=query) 
            product=Product.objects.filter(search).distinct()
            return product
        else:
            return Product.objects.filter(featured=True)
            
def searchposts(request):
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
    print("in cart")
    if request.method=='POST':
        product_id= request.POST.get('product_id')
        quantity= request.POST.get('quantity')
        product=Product.objects.get(id=product_id)
        cart= Cart.objects.filter(user=request.user , products=product).first()
        print(cart)
        if cart is not None:
            print(cart.total)
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
                return JsonResponse({"cartCount":request.user.carts.all().count()})
        
    return render(request, 'cart.html' ,{'cart':cart_obj})


class cartdelete(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        product=Product.objects.get(id=id1)
        cart=Cart.objects.filter(user=request.user , products=product)
        cart.delete()
        data = {
            'deleted': True,
            "cartCount":request.user.carts.all().count()
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


def order(request):
    if request.method=='POST':
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

        return redirect(cart)
    cart_obj=request.user.carts.all()
    return render(request, 'cart.html' ,{'cart':cart_obj})

def checkout(request):
    cart_obj=Cart.objects.filter(user=request.user)
    total=0
    for cart_total in cart_obj:
        total+= cart_total.total
    total= int(total)
    shipping=120

    gtotal= total + shipping

    user= User.objects.get(username=request.user)
    print("in checkoutt")
    context={
        "cart":cart_obj,
        "user":user,
        "total":total,
        "shipping":shipping,
        "Gtotal":gtotal
    }
    return render(request , 'checkout.html', context)