from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import login
from .models import Customer,Category,Product,Cart
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
     prod=Category.objects.all()
     return render(request,'index.html',{'prodct':prod})
 
def loginpage(request):
    return render(request,'login.html')


def signup(request):
    return render(request,'signup.html')


def login_check(request):
     if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
               
                login(request,user)
                return redirect('admin_home')
            else:
                login(request,user)
                auth.login(request,user)
                # messages.info(request,f'welcome {username}')
                return redirect('user_home')
        else:
           
            return redirect('loginpage')
     return render(request,'login.html')
 
@login_required(login_url="loginpage")
def admin_home(request):
    prod=Category.objects.all()
    return render(request,'adminhome.html',{'prodct':prod})

@login_required(login_url="loginpage")
def user_home(request):
    prshow=Product.objects.all()
    prod=Category.objects.all()
    return render(request,'userhome.html',{'show':prshow,'prodct':prod})


def user_signup(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        address=request.POST['address']
        email=request.POST['email']
        number=request.POST['number']
        img=request.FILES.get('file')
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        
        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                #print("Username already Taken..")
                return redirect('user_signup')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                user.save()
                u=User.objects.get(id=user.id)
                
                customer=Customer(address=address,contact=number,image=img,user=u)
                customer.save()
                return redirect('loginpage')
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            return redirect('user_signup')   
        return redirect('/')
    else:
        return render(request,'registration.html')

@login_required(login_url="loginpage")
def add_category(request):
    return render(request,'addcategory.html')


@login_required(login_url="loginpage")
def addcategory(request):
    if request.method=='POST':
        cat=request.POST['category']
        catg=Category(category=cat)
        catg.save()
        return redirect('add_category')
 
@login_required(login_url="loginpage")   
def addproduct(request):
    prod=Category.objects.all()
    return render(request,'addproduct.html',{'prodct':prod})

@login_required(login_url="loginpage")
def proadd(request):
    if request.method=='POST':
        pr=request.POST['addp']
        des=request.POST['desc']
        price=request.POST['price']
        img=request.FILES.get('img')
        sel=request.POST['sel']
        cat=Category.objects.get(id=sel)
        cat.save()
        product=Product(product=pr,description=des,price=price,image=img,category=cat)
        product.save()
        return redirect('showprdct')

@login_required(login_url="loginpage")
def showprdct(request):
    prod=Category.objects.all()
    pr=Product.objects.all()
    return render(request,'showproduct.html',{'prodct':prod ,'prdct':pr})

def logout(request):
    auth.logout(request)
    return redirect('index')

@login_required(login_url="loginpage")
def delete(request, pk):
    product_exists = Product.objects.filter(pk=pk).exists()
    if product_exists:
        product = Product.objects.get(pk=pk)
        product.delete()
        messages.success(request, 'Product deleted successfully.')
    else:
        messages.error(request, 'Product not found.')
    
    return redirect('showprdct')

@login_required(login_url="loginpage")
def user_details(request):
    details=Customer.objects.all()
    return render(request,'showusers.html',{'de':details})

@login_required(login_url="loginpage")
def delete_user(request, pk):
    user = User.objects.filter(id=pk)
    
    if user is not None:
        user.delete()
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, 'User not found.')
    
    return redirect('user_details') 


def categorized_products(request, category_id):
    categories = Category.objects.filter(id=category_id)
    
    if categories.exists():
        category = categories.first()
        products = Product.objects.filter(category=category)
        return render(request, 'categories.html', {'categories': [category], 'products': products})
    else:
        
        return render(request, 'user_home.html')

@login_required(login_url="loginpage")
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cartitems':cart_items,'totalprice': total_price})


@login_required(login_url="loginpage")
def cart_details(request, pk):
    product = Product.objects.get(id=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required(login_url="loginpage")
def removecart(request, pk):
    product = Product.objects.get(id=pk)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    
    if cart_item:
        cart_item.delete()
    
    return redirect('cart')
