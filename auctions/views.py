from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, User


def index(request): 
    if request.method == "POST":
        if request.user.is_authenticated:
            pk = request.POST['watchlist']
            product = Listing.objects.get(pk=pk)
            if product.watchlist_user.filter(pk=request.user.pk).exists():
                product.watchlist_user.remove(request.user)              
            else :
                product.watchlist_user.add(request.user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return HttpResponseRedirect(reverse("auctions:login"))
    return render(request, "auctions/index.html", {"listing" : Listing.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            heading = request.POST["heading"]
            name = request.POST["name"]
            description = request.POST["description"]
            category = request.POST.get("category")
            basebid = request.POST["base_bid"]
            image = request.FILES["image"]
            # if not category:
            #     return render(request, "auctions/new_listing.html", {"message" : "Please choose the category","listing":Listing.categories})
            new_listing = Listing(heading = heading, name = name , description = description, category =category, image =image, base_bid = basebid, listing_user = request.user)
            new_listing.save()
            return HttpResponseRedirect(reverse("auctions:listing",args=(new_listing.id,)) )
        return render(request, "auctions/new_listing.html", {"listing" : Listing.categories})
    return HttpResponseRedirect(reverse('auctions:login'))


def listing(request, listing_id):
    product = Listing.objects.get(pk = listing_id)
    if request.method == "POST":
        action  = request.POST.get("action")
        if action == "bid":
            if request.user.is_authenticated: 
                current_bid = request.POST["bid"]
                if current_bid == '':
                    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id, 'message':   "Please enter an amount"})
                elif int(current_bid) <= max(product.current_bid, product.base_bid):
                    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id,"message" :   "Price should be greator than the current bid"})
                else:
                    product.current_bid = int(current_bid)
                    product.number_of_bid += 1
                    product.save()
                    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id})
            return HttpResponseRedirect(reverse('auctions:login'))
        else :
            if request.user.is_authenticated:
                product = Listing.objects.get(pk=listing_id)
                if product.watchlist_user.filter(pk=request.user.pk).exists():
                    product.watchlist_user.remove(request.user)              
                else :
                    product.watchlist_user.add(request.user)
                return HttpResponseRedirect(reverse("auctions:listing" ,args=(listing_id,)))
            else:
                return HttpResponseRedirect(reverse("auctions:login"))

    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id})


def watchlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            pk = request.POST['watchlist']
            product = Listing.objects.get(pk=pk)
            product.watchlist_user.remove(request.user) 
            return HttpResponseRedirect(reverse("auctions:watchlist"))
        return render(request, "auctions/watchlist.html",{"listing": request.user.watchlist_user.all()})
    return HttpResponseRedirect(reverse("auctions:login"))
        

def categories(request):
    categorised = dict()
    for db_category ,category in Listing.categories:
        products = Listing.objects.filter(category=db_category)
        categorised[category] = products
    if request.method == "POST":
        categorised = dict()
        category = request.POST.get("category")
        catg = '' #Users category
        for db_catg , show_cat in Listing.categories:
            if category == db_catg:
                catg += show_cat
        products = Listing.objects.filter(category=category)
        categorised[category] = products
        return render(request, "auctions/categories.html", {"listing": Listing , "categorys" : categorised , "catg" : catg})
    return render(request, "auctions/categories.html", {"listing": Listing , "categorys" : categorised})