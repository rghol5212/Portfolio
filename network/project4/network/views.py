from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import JsonResponse
import json


def index(request):
    comments = Comments.objects.all()
    entries = Post.objects.all()
    if request.method == "POST":
        post = Post.objects.create(
            posts = request.POST['posts'],
            posts_owner = request.user
            )
        post.save()
        return render(request, "network/user_profile.html",
        {"entries" : entries,
        "comments" : comments}) 
    else:
        return render(request, "network/index.html",
        {"entries" : entries,
        "comments" : comments}) 
        
def vote_rating(request, posts_id):
    profile = User.objects.get(pk=request.user.pk)
    print('vote_rating function starting')
    post_linked = Post.objects.get(pk=posts_id)
    comments = Comments.objects.all()
    entries = Post.objects.all()
    if request.method != "POST":
        return render(request, "network/user_profile.html",
        {"entries" : entries,
        "comments" : comments,
        'profile' : profile}) 

    print(post_linked.rating)

    post_linked.rating = (int(request.POST['vote_input']) + post_linked.rating)
    post_linked.save()

    return render(request, "network/user_profile.html",
        {"entries" : entries,
        "comments" : comments,
        'profile' : profile}) 

#Fix a bug where where you need to track what url is 
# loaded when submitting comments and posts as not to 
# redirect just to the user_profile, but rather either to the 
# profile if needed to or to the all post if need be
#NON API View for comments
def comment(request, posts_id):
    print('comment function starting')
    post_linked = Post.objects.get(pk=posts_id)
    comments = Comments.objects.all()
    entries = Post.objects.all()
    if request.method != "POST":
        return render(request, "network/user_profile.html",
        {"entries" : entries,
        "comments" : comments}) 

    comment_data = request.POST["comment-input"]
    comment = Comments(
        user = request.user,
        comment = comment_data,
        post = post_linked
        )
    comment.save()

    return render(request, "network/user_profile.html",
        {"entries" : entries,
        "comments" : comments}) 


#API view for comment. CANT GET JS SCRIPT TO LOAD DUNNO IF WORKING
def comment_api(request):
    print('comment_api function starting')
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    print(request.POST)
    data = json.loads(request.body)
    print(data)
    comment_data = data.get("comment", "")
    comment = Comments(
        user = request.user,
        comment = comment_data,
    )
    comment.save()

    return JsonResponse({"message": "Comment Submitted."}, status=201)


def following_list(request, user_id):
    profile = User.objects.get(pk=user_id)
    following = profile.following.all()
    return render(request, "network/following.html",
    {"profile" : profile,
    'following' : following}) 


def follow(request, user_id):
    profile = UserProfile.objects.get(pk=user_id)
    profile.following.add(request.user)
    return redirect('user_profile', user_id=profile.pk)

def unfollow(request, user_id):
    profile = UserProfile.objects.get(pk=user_id)
    profile.following.remove(request.user)
    return redirect('user_profile', user_id=profile.pk)

def user_profile(request, user_id):
    profile = UserProfile.objects.get(pk=user_id)
    user = profile.user
    entries = Post.objects.all()
    following = profile.following.all()
    comments = Comments.objects.all()
    is_following = False

    for followed in following:
        if followed == request.user:
            is_following = True
            break
        else:
            is_following = False
 
    number_of_following = len(following)

    if request.method == "POST":
        post = Post.objects.create(
            posts = request.POST['posts'],
            posts_owner = request.user
            )
        post.save()
        return render(request, "network/user_profile.html",
        {"entries" : entries,
        "comments" : comments,
        'user': user,
        'profile': profile,
        'is_following': is_following,
        'number_of_following': number_of_following,}) 

    else:
        return render(request, "network/user_profile.html",
        {"entries" : entries,
        "comments" : comments,
        'user': user,
        'profile': profile,
        'is_following': is_following,
        'number_of_following': number_of_following,}) 



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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
