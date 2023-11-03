from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
from user_app.models import Customer


# Home view.
@cache_control(no_cache=True,must_revalidate=True, no_store=True)
@login_required(login_url='loginpage')
def HomePage(request):
    if 'username' in request.session:
        return render(request, 'home.html')
    else:
        return redirect('loginpage')
    

    

# Signup view
@cache_control(no_cache=True, no_store=True)
def SignupPage(request):
    if 'username' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            # name = request.POST.get('name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            c_password = request.POST.get('cpassword')

            exist_username = User.objects.filter(username=username)
            exist_email = User.objects.filter(email=email)
            # checking the username is exist or not
            if exist_username.exists():
                messages.error(request, "username is already taken, try another")
                return redirect('signup')

            # checking the email is exist or not
            if exist_email.exists():
                messages.error(request, "email is already taken")
                return redirect('signup')
            if password == c_password:
                my_user = User.objects.create_user(username=username, password=password, email=email)
                my_user.save()
                new_user = Customer()
                new_user.name = username 
                new_user.user_name = username
                new_user.email = email
                new_user.save()
                messages.success(request, "User created successfully ")
                return redirect('loginpage')
            else:
                messages.error(request, "Password didn't match, try again")
                return redirect('signup')

    return render(request, 'signup.html')


#Login View
@cache_control(no_cache=True, no_store=True)
def Loginpage(request):
    if 'email' in request.session:
        return redirect('admin_home')
    if 'username' in request.session:
        return redirect('home')
    else:
        if request.method == 'POST':
            try:
                username = request.POST['username']
            except:
                print("username error")
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                request.session['username'] = username
                login(request, user)
                
                return redirect('home')
            else:
                messages.error(request, "Username and password not matching")
                return redirect('loginpage')
    return render(request, 'loginpage.html')



# @cache_control(no_cache=True, no_store=True)
# @login_required(login_url='loginpage')
# def LogoutPage(request):
#     if 'username' in request.session:
#         auth.logout(request)
#         print("not working")
#         # request.session.flush()
#     return redirect('loginpage')

# @cache_control(no_cache=True, must_revalidate=True,no_store=True)

# Logout View
# @login_required(login_url='loginpage')
# def LogoutPage(request):
#     if 'username' in request.session:
#         auth.logout(request)
#         return redirect('loginpage')
    # else:
    #     return redirect('loginpage')
    
@login_required(login_url='loginpage')
def LogoutPage(request):
    auth.logout(request)
    # print(request.session['username'])
    return redirect('loginpage')