from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm, ItemImageFormSet, ItemImage
from django.contrib.auth.decorators import login_required
from .models import User
from .models import Item
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ItemForm, ItemImageFormSet
from django.utils import timezone
from datetime import timedelta


def index(request):
    return render(request, "warehouse_platform/index.html", {
        "warehouse_platform": Item.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "warehouse_platform/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "warehouse_platform/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        user_type = int(request.POST["user_type"])  # Assume this comes from a dropdown in the form

        if password != confirmation:
            return render(request, "warehouse_platform/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.user_type = user_type
            user.save()
        except IntegrityError:
            return render(request, "warehouse_platform/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "warehouse_platform/register.html")

    
def index(request):
    return render(request, "warehouse_platform/index.html", {
        "warehouse_platform": Item.objects.all()
    })


def item(request, item_id):
    item = Item.objects.get(pk=item_id)
    return render(request, "warehouse_platform/item.html", {
        "item": item
    })

def item_list(request):
    items = items.objects.all()
    return render(request, 'warehouse_platform/item_list.html', {'items': items, 'add_item_url': '/add_item/'})




@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()

            # Handle multiple images
            images = request.FILES.getlist('images')  # Get the list of files from 'images' field
            for image in images:
                ItemImage.objects.create(item=item, image=image)  # Create an ItemImage instance for each image

            return redirect('item', item_id=item.id)
    else:
        form = ItemForm()

    return render(request, 'warehouse_platform/add_item.html', {'form': form})











@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # Allow both the item owner and superusers to edit the item
    if not (request.user.is_superuser or (item.owner == request.user and request.user.user_type == 2)):
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item', item_id=item.id)
    else:
        form = ItemForm(instance=item)

    return render(request, 'warehouse_platform/edit_item.html', {
        'form': form,
        'item': item
    })



@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # Allow both the item's owner and superusers to delete the item
    if not (request.user.is_superuser or item.owner == request.user):
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        item.delete()
        return redirect('item_list')  # Redirect to the listing page or an appropriate page

    return render(request, 'warehouse_platform/confirm_delete.html', {'item': item})


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:  # Ensure only admins can access this page
        return HttpResponse("Unauthorized", status=401)

    items = Item.objects.all().select_related('owner')  # Fetch all items and their related owners
    return render(request, 'warehouse_platform/admin_dashboard.html', {'items': items})


@login_required
def rent_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST' and item.is_rented == False:
        rental_period = request.POST.get('rental_period')
        if rental_period == 'weekly':
            duration = timedelta(weeks=1)
        elif rental_period == 'monthly':
            duration = timedelta(weeks=4)
        elif rental_period == 'yearly':
            duration = timedelta(weeks=52)
        else:
            return HttpResponse("Invalid rental period", status=400)

        item.is_rented = True
        item.rented_by = request.user
        item.rental_end_date = timezone.now() + duration
        item.save()
        return redirect('manage_my_rentals')

    return render(request, 'warehouse_platform/rent_item.html', {'item': item})

@login_required
def manage_my_rentals(request):
    current_rentals = Item.objects.filter(rented_by=request.user, rental_end_date__gte=timezone.now())
    past_rentals = Item.objects.filter(rented_by=request.user, rental_end_date__lt=timezone.now())
    return render(request, 'warehouse_platform/manage_my_rentals.html', {
        'current_rentals': current_rentals,
        'past_rentals': past_rentals
    })

@login_required
def manage_my_listings(request):
    if request.user.user_type != 2:
        return HttpResponse("Unauthorized", status=401)
    listings = Item.objects.filter(owner=request.user)
    return render(request, 'warehouse_platform/manage_my_listings.html', {'listings': listings})





