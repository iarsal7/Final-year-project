from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView
from .forms import SignUpForm , CustomerForm , SearchForm
from .models import Product
from django.db.models import Q
from django.contrib import messages

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
            query= Q(title__icontains=search) | Q(description__icontains=search)
            products= Product.objects.filter(query).distinct()

            context={'products': products,
                     'submit': submit}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')
