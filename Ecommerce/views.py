from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView
from .forms import SignUpForm , CustomerForm , SearchForm
from .models import Product , Cart , Order ,OrderDetail
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
def home(request):
    context={
        "title":"hello world"

    }
    return render(request, 'home.html',context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        Customer_Form = CustomerForm(request.POST or None)
        if form.is_valid() and Customer_Form.is_valid():
            user = form.save()
            customer= Customer_Form.save(commit=False)
            customer.user=user
            customer.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        Customer_Form = CustomerForm()
        
    return render(request, 'signup.html', {'form': form , 'Cform' : Customer_Form})


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
    
    if request.method=='POST':
        cart_obj= Cart.objects.create(user= request.user)
        product_id= request.POST.get('product_id')
        quantity= request.POST.get('quantity')
        product=Product.objects.get(id=product_id)
        cart_obj.products=product
        cart_obj.quantity=quantity
        total=Decimal(cart_obj.quantity) * product.price
        cart_obj.total= total
        cart_obj.save()
        return redirect(cart)
    return render(request, 'cart.html' ,{'cart':cart_obj})

def cartUpdate(request):
    if request.method=='POST':
        product_id= request.POST.get('product_id')
        product=Product.objects.get(id=product_id)
        cart=Cart.objects.filter(user=request.user , products=product)
        cart.delete()
        
    cart_obj=request.user.carts.all()

    return render(request , 'cart.html', {'cart':cart_obj})

def checkout(request):
    if request.method=='POST':
        order_obj= Order.objects.create(user= request.user)
        order_obj.shippingtotal=120.00
        total=0
        cart_obj=Cart.objects.filter(user=request.user)
        for cart_total in cart_obj:
            total+= cart_total.total
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