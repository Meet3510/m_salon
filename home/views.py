from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages


from .models import register


def logouthandle(request):
    logout(request)
    return redirect(('/home'))


def home(request):
    return render(request, 'index.html')



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['pass']

        phone = request.POST['phone']
        confirm = request.POST['pass']
        # validations
        if len(username) < 3:
            messages.warning(request, "Username must be greater than 3 characters ")
            return render(request, 'regi.html')
        if not username.isalnum():
            messages.warning(request, "Username only contain letter and numbers ")
            return render(request, 'regi.html')
        if password != confirm:
            messages.warning(request, "passwords do not match ")
            return render(request, 'regi.html')
        if len(email) < 6:
            messages.warning(request, "Email must be greater than 6 letter")
            return render(request, 'regi.html')
        if len(password) < 8:
            messages.warning(request, " Password Must be 8 Char long ")
            return render(request, 'regi.html')
        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email Already Exists Try Another One")
            return render(request, 'regi.html')
        if User.objects.filter(username=username).exists():
            messages.warning(request,"Username Already Exists Try Another One")
            return render(request, 'regi.html')
        else:

            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            x1 = register(username=username, lastname=lastname, email=email,
                      phone=phone, password=password, confirm=confirm)
            x1.save()
            messages.success(request,'Register Successfully')
            return redirect('/login')

    else:
        return render(request, 'regi.html')



def loginhandle(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')

        x = authenticate(username=loginusername, password=loginpassword)
        print(x)
        if x is not None:
            login(request, x)
            messages.success(request, 'Login Successfully')
            return redirect('/home', x)
        else:
            messages.warning(request, 'invalid username or password')
            return redirect("loginhandle")
    else:
        return render(request, 'login.html')



def login1(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('loginusername')
        password = request.POST.get('loginpassword')
        customer = register.get_customer_by_username(username)

        err_msg = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['loginusername'] = customer.username;
                request.session['first_name'] = customer.first_name;
                request.session['last_name'] = customer.last_name;
                return render(request, 'index.html', {'customer': customer})
            else:
                err_msg = 'Email or Password Invalid !!'
        else:
            err_msg = 'Email or Password Invalid !!'
        print(customer)
        print(username, password)
        return render(request, 'login.html', {'err': err_msg, 'customer': customer})



def updateprofile(request):
    user = User.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        lastname = request.POST['lastname']
        mobile = request.POST['mobile']
        email = request.POST['email']
        user.username = username
        user.save(update_fields=['username'])
        user.lastname = lastname
        user.save(update_fields=['lastname'])
        user.mobile = mobile
        user.save(update_fields=['mobile'])
        user.email = email
        user.save(update_fields=['email'])
        user.save()
        messages.info(request, 'You have successfully update profile!!')
        return redirect('/myprofile')
    else:
        return render(request, 'editprofile.html')


def adminlogin(request):
    if request.method == 'POST':
        adminname = request.POST.get('adminname')
        password = request.POST.get('password')
        print(adminname,password)
        if (adminname =='admin1'):
            if(password =='admin'):
                return redirect('/dashboard')
            else:
                messages.info(request, 'invalid username or password')
                return redirect("adminlogin")
        else:
            messages.info(request, 'invalid username or password')
            return redirect("adminlogin")
    else:
        return render(request, 'admin_login.html')