from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from math import ceil


def home(request):
    allProds = []
    # Geting categories
    catprods = product.objects.values('category').distinct()
    categories = [item['category'] for item in catprods]

    for cat in categories:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        
        # creating list of lists
        prod_chunks = [prod[i:i + 4] for i in range(0, n, 4)]
        allProds.append([cat, prod_chunks])
    params = {
        'allProds': allProds
        }
    return render(request, "store/home.html", params)


def product_listing(request):
    products = list(product.objects.all())
    pag = Paginator(products,12)
    page_number = request.GET.get('page')
    products_final = pag.get_page(page_number)
    total_pages = pag.num_pages
    params = {'products': products,
              'paginated_products': products_final,
              'lastpage':total_pages,
              'totalpageslist':[n+1 for n in range(total_pages)]
              }
    return render(request, "store/productlisting.html",params)


def product_details(request, myid):
    products = product.objects.filter(id = myid)
    params ={'products': products}
    return render(request,"store/productdetails.html",params)


def search(request):
    query = request.GET.get('query')
    if len(query) < 50:
        searched_products = product.objects.filter(name__icontains=query)
    else:
        searched_products = []
    params = {'searched_products': searched_products,
              'query': query}
    return render(request,"store/search.html",params)


def submit_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # checking existance of username 
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exist")
            return redirect("/")
        # checking len of username
        if len(username) < 8:
            messages.error(request,"Usernames should be greater than 8 characters")
            return redirect("/")
        # check for special symbols
        if not username.isalnum():
            messages.error(request,"Spaces and special symbols (@,$,^,&) not allowed")
            return redirect("/")
        # matching password
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("/")
        # creating user
        newuser = User.objects.create_user(username,email,password1)
        newuser.first_name = fname
        newuser.last_name = lname
        newuser.save()
        messages.success(request,"Account has been created successfully")
        return redirect("/")
    else:
        return HttpResponse("page not found")


def submit_login(request):
    if request.method=='POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request,"Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid credentials...")
            return redirect("/")


def submit_logout(request):
    logout(request)
    messages.success(request,"Logged out succesfully")
    return redirect("/")


def about(request):
    return render(request, "store/about.html")
# Create your views here.
