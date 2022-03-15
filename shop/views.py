from nis import cat
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from datetime import date, timedelta
from django.db import IntegrityError

from .models import *

def home(request):
    home = Home.objects.all().first()
    context = {
        'home': home
    }
    return render(request, 'shop/home.html', context)

def stock(request):
    categories = Category.objects.all().order_by('-id')
    items = Stock.objects.all().order_by('-id')

    if request.GET.get('category'):
        has_category = Category.objects.filter(name=request.GET.get('category')).first()
        if has_category:
            items = items.filter(category=has_category)

    context = {
        'categories': categories,
        'items': items,
        'current': request.GET.get('category'),
    }
    return render(request, 'shop/stock.html', context)

def item(request, id):
    # post review
    if request.user.is_authenticated:
        if request.method == 'POST':
            has_reviewd = Review.objects.filter(reviewer__username=request.user.username).first()
            if has_reviewd:
                messages.add_message(request, messages.WARNING, "You have already reviewd!")
            else:
                if request.POST.get('review'):
                    Review.objects.create(
                        reviewer=request.user,
                        review_on=Stock.objects.filter(id=id).first(),
                        review=request.POST.get('review'),
                        star=5
                    )
                    messages.add_message(request, messages.SUCCESS, "Review has been posted successfully!")

    reviews = Review.objects.filter(review_on__id=id)
    item = Stock.objects.filter(id=id).first()
    items = Stock.objects.all()[:6]

    is_purchased = Order.objects.filter(user=request.user).first()

    if not item:
        raise Http404
        
    context = {
        'item': item,
        'items': items,
        'reviews': reviews,
        'is_purchased': is_purchased,
    }
    return render(request, 'shop/item.html', context)

def pricing(request):
    is_purchased=False
    if request.user.is_authenticated:
        status = request.GET.get('status')
        tran_id = request.GET.get('transaction_id')
        plan = request.GET.get('plan')

        if plan == 'Basic':
            paid = 10
        elif plan == 'Creator':
            paid = 25
        else:
            paid = 35
        days_after = (date.today()+timedelta(days=30)).isoformat()
        try: 
            if status and tran_id and plan:
                Order.objects.create(
                    user=request.user,
                    paid=paid,
                    expires = days_after
                )
        except IntegrityError:
            messages.add_message(request, messages.ERROR, "You already purchased a plan.!")
            return redirect('/pricing/')
        is_purchased = Order.objects.filter(user=request.user).first()

    reviews = Review.objects.all().order_by('-at')[:3]

    context = {
        'is_purchased': is_purchased,
        'reviews': reviews,
    }
    return render(request, 'shop/pricing.html', context)

def testimonials(request):
    reviews = Review.objects.all().order_by('-at')[:3]
    context = {
        'reviews': reviews
    }
    return render(request, 'shop/testimonials.html', context)





# admin area
def admin_area(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('baseline') and request.POST.get('facebook') and request.POST.get('twitter') and request.POST.get('instagram') and request.POST.get('vemio') and request.POST.get('pinterest'):
            inc = Home.objects.all().first()
            inc.title = request.POST.get('title')
            inc.baseline = request.POST.get('baseline')
            inc.facebook = request.POST.get('facebook')
            inc.twitter = request.POST.get('twitter')
            inc.instagram = request.POST.get('instagram')
            inc.vemio = request.POST.get('vemio')
            inc.pinterest = request.POST.get('pinterest')
            inc.save()
            messages.add_message(request, messages.SUCCESS, "Successfully Saved")
            return redirect('/admin-area/')
        else:
            messages.add_message(request, messages.SUCCESS, "All te fields are required!")

    home = Home.objects.all().first()

    context = {
        'home': home
    }
    return render(request, 'shop/admin/admin_area.html', context)

def admin_stock(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_superuser:
        return redirect('/')

    
    if request.method == 'POST':
        # create a category
        if request.POST.get('new_category'):
            has_already = Category.objects.filter(name=request.POST.get('new_category')).first()
            if has_already:
                messages.add_message(request, messages.ERROR, 'Category already exists with this name.')
                return redirect('/admin-area/stock/')
            else:
                Category.objects.create(name=request.POST.get('new_category'))
                messages.add_message(request, messages.SUCCESS, 'Category has been created successfully!')
                return redirect('/admin-area/stock/')

        # create a stock item
        name = request.POST.get('name')
        description = request.POST.get('description')
        detail = request.POST.get('detail')
        category = request.POST.get('category')
        preview = request.FILES.get('preview')
        work = request.FILES.get('work')
        license = request.FILES.get('license')
        if name and description and detail and category and preview and work and license:
            has_category = Category.objects.filter(id=category).first()
            if has_category:
                Stock.objects.create(
                    name=name,
                    description=description,
                    detail=detail,
                    category=has_category,
                    preview=preview,
                    download=work,
                    license=license
                )
                messages.add_message(request, messages.SUCCESS, "Stock item has been added successfully!")
                return redirect('/admin-area/stock/')

    # all categories
    categories = Category.objects.all().order_by('-id')
    # all items
    items = Stock.objects.all().order_by('-id')
    context = {
        'categories': categories,
        'items': items
    }
    return render(request, 'shop/admin/admin_stock.html', context)

def admin_order(request):
    if not request.user.is_authenticated:
        return redirect('/')
    if not request.user.is_superuser:
        return redirect('/')


    orders = Order.objects.all().order_by('-id')
    context = {
        'orders': orders
    }
    return render(request, 'shop/admin/orders.html', context)