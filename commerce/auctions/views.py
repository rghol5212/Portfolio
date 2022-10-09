from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required



def index(request):
    entries =  ActiveListing.objects.all()
    return render(request, "auctions/index.html",
    {'entries': entries}
    )

@login_required
def getuser(request, entrydetail):
    entry= ActiveListing.objects.get(name_of_listing = entrydetail)
    new_comment = Comments(id=None, listing = entry, user=request.user, comment="This is a comment posted by a user" )
    new_comment.save()

@login_required
def getcategory(request, category):
    allentry = ActiveListing.objects.all()
    print(category)
    return render(request, "auctions/categories.html",
    {'allentry': allentry,}
        )
        


#Individual items page and bid form
@login_required
def entrydetail(request, entrydetail):
    entry = ActiveListing.objects.get(name_of_listing = entrydetail)
    comments = Comments.objects.filter(listing=entry.id)
    list_id = ActiveListing.objects.get(name_of_listing = entrydetail)
    watchlist = Watchlist.objects.filter(listing_id=entry.id)
    watchlist = watchlist.filter(user_id=request.user.id)
    if request.user==entry.upload_author:
        uploaded_author = True
    else:
        uploaded_author = False
    current_user = request.user


    if request.method == "POST":
        #if the start price input field was submitted and is apart of the post data run this code:
        if "start_price" in request.POST:
            if entry.start_price < int(request.POST["start_price"]):
                entry.start_price = request.POST["start_price"]
                entry.number_of_bids += 1
                entry.highest_bidder = request.user
                entry.save()
                return render(request, "auctions/entrydetail.html",
                {'entry': entry,
                'comments': comments,
                'uploaded_author' : uploaded_author,
                'current_user': current_user,}
                )
            else:
                return HttpResponse("Bid HIGHER then current bid")
        #if the watch list button is pressed and is added to the post data run this:
        elif "watchlistaddbtn" in request.POST:
            print("watch list button true")
            watchlist_list = Watchlist.objects.filter(user_id=request.user.id)
            print(watchlist_list)
            for watched_entry in watchlist_list:                
                if list_id.id == watched_entry.listing_id and request.user.id == watched_entry.user_id:
                    print("already on watchlist")
                    
                    watched_entry.delete()
                    print("deleted from watchlist")
                    print(watched_entry)
                    return render(request, "auctions/entrydetail.html",
                    {'entry': entry,
                    'comments': comments,
                    'uploaded_author' : uploaded_author,
                    'current_user': current_user,
                    'watched_entry': "None",}
                     )
        
    
            print("adding to watchlist")
            Watchlist.objects.create(listing_id=list_id.id, user_id=request.user.id)
    
            return render(request, "auctions/entrydetail.html",
            {'entry': entry,
            'comments': comments,
            'uploaded_author' : uploaded_author,
            'current_user': current_user,
            'watched_entry':  watchlist[0],}
            )
        #If a comment was made and input comment_input was in the post data
        elif "comment_input" in request.POST:
            Comments.objects.create(listing_id=list_id.id, user_id=request.user.id, comment=request.POST["comment_input"])
            print('done creating new comment')
            return render(request, "auctions/entrydetail.html",
            {'entry': entry,
            'comments': comments,
            'uploaded_author' : uploaded_author,
            'current_user': current_user,}
            )
        #If Close the list was pressed. This is only able to be pressed by the author of the listing
        elif "closelisting" in request.POST:
            # watched_entry = Watchlist.objects.filter(user_id=request.user.id)
            # watched_entry = watched_entry.filter(listing_id=entry.id)
            entry.is_sold = True
            entry.save()
            return render(request, "auctions/entrydetail.html",
            {'entry': entry,
            'comments': comments,
            'uploaded_author' : uploaded_author,
            'current_user': current_user,
            'watched_entry':  "None",}
            )


        else:
            print("skipped everything")
            return render(request, "auctions/entrydetail.html",
            {'entry': entry,
            'comments': comments,
            'uploaded_author' : uploaded_author,
            'current_user': current_user,}
            )
    #Load the details page, method is GET.
    else:
        if len(watchlist) >= 1:
            watched_entry = watchlist[0]
        else:
            watched_entry = "None"
        print("load page...method is GET")
        return render(request, "auctions/entrydetail.html",
        {'entry': entry,
        'comments': comments,
        'uploaded_author' : uploaded_author,
        'current_user': current_user,
        'watched_entry': watched_entry,
         }
        )

#Users profile page that lists all there watchlist items.
@login_required
def watchlist(request):
    entries =  Watchlist.objects.filter(user_id=request.user.id)
    entry_list = []
    for y in entries:
        entryid = y.listing_id
        entry = ActiveListing.objects.get(pk=entryid)
        entry_list.append(entry)

    if request.method == "POST":
        pass
    else:
        return render(request, "auctions/watchlist.html",
        {'entries': entry_list}
        )

@login_required
def categories(request):
    if request.method == "POST":
        entries =  ActiveListing.objects.filter(categories_id=request.POST["categories_id"])
        print("going post")
        print(entries)
        print(len(entries))
        return render(request, "auctions/categories.html",
            {'entries': entries}
            )
    else:
        entries =  ActiveListing.objects.all()
        return render(request, "auctions/categories.html",
            {'entries': entries}
            )

    
@login_required    
def createlisting(request):
    if request.method == "POST":    
        category_choice = Categories.objects.get(pk=request.POST["category"])
        print(category_choice.category)
        entry_db = ActiveListing.objects.create(
            name_of_listing = request.POST["name_of_listing"],
            start_price = request.POST["start_price"],
            description = request.POST["description"],
            # created_date = request.POST["created_date"],
            categories = category_choice,
            image = request.POST["img_url"],
            highest_bidder = request.user,
            upload_author = request.user,
            is_sold = False,
        )
        entry_db.save()
        return index(request)
    else:
        return render(request, "auctions/createlisting.html",
        {}
        )



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
