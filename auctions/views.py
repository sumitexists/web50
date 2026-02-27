from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, User, comments, winner


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
    return render(request, "auctions/index.html", {"listing" : Listing.objects.all(), "bidding" : winner.objects.all()})


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
    if request.user.is_authenticated:
        user = request.user
    else :
        user = None
    product = Listing.objects.get(pk = listing_id)
    if product.listing_name.exists():
        top_winner_list = product.listing_name.order_by("-current_bid").first()
        top_winner = top_winner_list.current_bid
    else:
        top_winner = 0
    
    if request.method == "POST":
        action  = request.POST.get("action")
        if action == "bid":
            if request.user.is_authenticated: 
                current_bid = request.POST["bid"]
                if current_bid == '':
                    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id, 'message':   "Please enter an amount"})
                elif int(current_bid) <= max(top_winner, product.base_bid):
                    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id,"message" :   "Price should be greator than the current bid"})
                else:
                    if(product.listing_name.exists()):
                        bidder = winner.objects.get(listing = product)
                        bidder.current_bid = int(current_bid)
                        bidder.listing = product
                        product.number_of_bid += 1
                        bidder.save()
                        product.save()
                    else:
                        bidder = winner.objects.create(listing = product , winner = request.user , current_bid = int(current_bid))
                    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id})
            return HttpResponseRedirect(reverse('auctions:login'))
        elif action == "watchlist":
            if request.user.is_authenticated:
                product = Listing.objects.get(pk=listing_id)
                if product.watchlist_user.filter(pk=request.user.pk).exists():
                    product.watchlist_user.remove(request.user)              
                else :
                    product.watchlist_user.add(request.user)
                return HttpResponseRedirect(reverse("auctions:listing" ,args=(listing_id,)))
            else:
                return HttpResponseRedirect(reverse("auctions:login"))
        elif action == "comment":
            comment = request.POST['comments'] 
            user = request.user
            save_comment = comments(commented_user = user , product = Listing.objects.get(pk = listing_id) , comment= comment)
            save_comment.save()
        
    return render(request, "auctions/listing.html" , {"product" : product , "listing_id" : listing_id, "comments": comments.objects.filter(product = listing_id) , "user" : user})


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