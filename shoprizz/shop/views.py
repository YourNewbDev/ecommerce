from django.shortcuts import render, redirect
from . models import Product, Category, Order, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . forms import RegisterForm, SearchForm
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    products = Product.objects.all().order_by('id')

    # Pagination
    paginator = Paginator(products, 8) # Number of products per page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        products = paginator.page(1)

    except EmptyPage:
        # If page is out of range, deliver the last page of results
        products = paginator.page(paginator.num_pages)


    return render(request, 'index.html', {'products':products})

def about(request):

    return render(request, 'about.html', {})

def product(request, pk):
    product = Product.objects.get(id=pk)

    return render(request, 'product.html', {'product':product})

def category(request, name):
    category = get_object_or_404(Category, name=name)
    products = Product.objects.filter(category=category).order_by('id')

    # Pagination
    paginator = Paginator(products, 8) # Number of products per page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        products = paginator.page(1)

    except EmptyPage:
        # If page is out of range, deliver the last page of results
        products = paginator.page(paginator.num_pages)


    return render(request, 'category.html', {'category': category, 'products': products})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            messages.success(request, ("You have successfully logged in!"))
            return redirect('index')

        else:
            messages.success(request, ("Username or password error, please try again."))
            return redirect('login') 

    else:
        return  render(request, 'login.html', {})

def logout_user(request):
    logout(request)

    messages.success(request, ("Your account have been logged out."))
    return redirect('index')

def register_user(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, ("You have registered successfully!"))
            return redirect('index')
        
        else:
            messages.success(request, ("Oops. There was an error upon registration, please try again."))
            return redirect('register') 

    else:
        return render(request, 'register.html', {'form': form})
    
def search_product(request):
    form = SearchForm(request.GET)
    query = form['query']

    if form.is_valid() and query:
        products = Product.objects.filter(name__icontains=query)

        # Pagination
        paginator = Paginator(products, 8)
        page = request.GET.get('page')

        try:
            products_page = paginator.page(page)
        
        except PageNotAnInteger:
            products_page = paginator.page(1)
        
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        return render(request, 'search.html', {'query': query, 'products': products_page, 'form': form})
    
    
    return render(request, 'search.html', {'query': '', 'products': [], 'form': form})
    
    # if request.method == 'POST':
    #     query = request.POST['query']
    #     products = Product.objects.filter(name__icontains=query)

    #     return render(request, 'search.html', {'query': query, 'products': products})
    
    # else:
    #     return redirect('search')