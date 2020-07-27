from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    if request.user.is_authenticated:
        return render(request, "network/index.html",{
            "posts": Post.objects.all()
        })
    else:
        return HttpResponseRedirect(reverse("login"))

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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newPost(request):
    post = Post()
    try:
        usr = User.objects.get(username=request.user.username)
    except KeyError:
        return render(request, "network/error.html", {"message": "User not found"})
    except User.DoesNotExist:
        return render(request, "network/error.html", {"message": "User not found"})
    post.author = usr
    # post.datetime = set by defaul
    post.content = request.POST["content"]
    # totallikes = (default=0)
    post.save()
    return HttpResponseRedirect(reverse("index"))

def profile(request):
    '''
    Profile Page: 
    - Display the number of followers the user has, as well as the number of people that the user follows.
    - Display all of the posts for that user, in reverse chronological order.
    - For any other user who is signed in, this page should also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.
    '''
    if request.method == "GET":
        # Display info
        usrCurrent = User.objects.get(username=request.user.username) # Get current user objet
        usrAll = User.objects.exclude(username= request.user.username) # Get users list, without current user
        numFollowers = usrCurrent.user_set.all().count() # Get number of followers of current user
        followed = usrCurrent.follows.all()
        numFollowed = followed.count() # Get number of users the current user follows
        posts = sorted(Post.objects.filter (author=usrCurrent), key=lambda x: x.datetime, reverse=True) # Get posts of current user; first the recentest
        return render(request, "network/profile.html", {
            "usrCurrent": usrCurrent,
            "usrAll": usrAll,
            "numFollowers": numFollowers,
            "numFollowed": numFollowed,
            "followed": list(followed),
            "posts": posts
        })
    else:
        # Update followed list
        usrCurrent = User.objects.get(username=request.POST["usrCurrent"])
        followedList = request.POST.getlist('followed',None)
        if followedList is not None:
            # First clear the followed list 
            usrCurrent.follows.clear()
            # Now recreate the followed list 
            for username in followedList:
                usr = User.objects.get(username=username)
                usrCurrent.follows.add(usr)
            usrCurrent.save()
        return HttpResponseRedirect(reverse("profile"))