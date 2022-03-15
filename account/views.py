from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as log_out
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        first = request.POST.get('first')
        last = request.POST.get('last')
        username = request.POST.get('username')
        email =request.POST.get('email')
        password = request.POST.get('password')
        if first and last and username and email and password:
            has_user = User.objects.filter(username=username).first()
            if has_user:
                messages.add_message(request, messages.ERROR, 'Username already exists!')
                return redirect('/auth/signup/')
            has_email = User.objects.filter(email=email).first()
            if has_email:
                messages.add_message(request, messages.ERROR, 'Email already exists!')
                return redirect('/auth/signup/')
            
            user = User.objects.create_user(username, email, password)
            user.first_name = first
            user.last_name = last
            user.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Account has been created successfully!')
            return redirect('/')

    context = {
    }
    return render(request, 'account/signup.html', context)

def log_in(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            u=authenticate(username=username, password=password)
            if u:
                login(request, u)
                messages.add_message(request, messages.SUCCESS, 'Login successfull.')
                return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password')
                return redirect('/auth/login/')

    context = {

    }
    return render(request, 'account/login.html', context)

def logout(request):
    if request.user.is_authenticated:
        log_out(request)
        messages.add_message(request, messages.SUCCESS, 'Logout successfull.')
        return redirect('/')
