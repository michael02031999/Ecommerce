from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from .models import User, auction_listing, bid, comment, watchlist



def watchlist_items(request):
            
            #watchlist.objects.create(auction_id=request.POST.get("auction_id"), user=request.POST.get("user"))       

    watchlist_items = watchlist.objects.filter(user=request.user)

    auction_list=[]

    for item in watchlist_items:
        auction_item = auction_listing.objects.filter(id = item.auction_id)
        auction_list.append(auction_item[0])


    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items,
        "count": watchlist_items.count(),
        "auction_list": auction_list
    })

def listing_page(request, auction_id):

    a = auction_listing.objects.filter(id=auction_id)
    watchlist_items = watchlist(user=request.user)
    w_items = watchlist.objects.filter(user=request.user)
    watchlist_items = watchlist.objects.filter(user=request.user)
    

    all_elements= { "auction_listing": a[0],
                "watchlist_items": watchlist_items,
                "auction_id": auction_id}

    all_elements["count"] = watchlist_items.count() 

    if request.method == "POST":
        
        try: 
            bid = int(request.POST.get("bid"))
            print(bid)
        except: 
            print("An error has been thrown")



















        
        if request.POST.get("AddRemove") == "Remove from watchlist":
            watchlist_items = watchlist.objects.filter(user=request.user)
            all_elements["AddRemove"] = "Add to watchlist"
            watchlist.objects.filter(auction_id=auction_id).delete()
            all_elements["count"] = watchlist_items.count()
            return render(request, "auctions/listing_page.html", all_elements)
        else:
            watchlist_items = watchlist.objects.filter(user=request.user)
            all_elements["AddRemove"] = "Remove from watchlist"
            user = str(request.user)
            newlist = watchlist.objects.create(auction_id = auction_id, user = user)
            watchlist.save(newlist)
            all_elements["count"] = watchlist_items.count()
            return render(request, "auctions/listing_page.html", all_elements)

    if request.method == "GET":
        for w_item in w_items:
            if w_item.auction_id == auction_id:
                all_elements["AddRemove"] = "Remove from watchlist"
                return render(request, "auctions/listing_page.html", all_elements)

        all_elements["AddRemove"] = "Add to watchlist"
        return render(request, "auctions/listing_page.html", all_elements)

def create_list(request):
    watchlist_items = watchlist.objects.filter(user=request.user)

    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = request.POST.get("starting_bid")
        url = request.POST.get("url")
        category = request.POST.get("category")

        #You left off right here trying to access the database !
        
        a = auction_listing(user = user, title=title, description=description, starting_bid=starting_bid, url=url, category=category)
        a.save()

        return HttpResponseRedirect(reverse("index"))

        #return render(request, "auctions/index.html")

    return render(request, "auctions/create_list.html", {
         "count": watchlist_items.count()
    })

def index(request):
    auctions = auction_listing.objects.all()
    watchlist_items = watchlist.objects.filter(user=request.user)

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "count": watchlist_items.count()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
