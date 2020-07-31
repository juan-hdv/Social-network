from django.db import IntegrityError, Error
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
import json
from .models import User, Post

CONST_linesPerPage = 10

def index(request):
    if request.user.is_authenticated:
        usrCurrent = User.objects.get(username=request.user.username) # Get current user object
        post = Post.objects.all().order_by(F('datetime').desc()) # All posts (with total likes)
        paginator = Paginator(post, CONST_linesPerPage) # Show  CONST_linesPerPage libes per page.

        return render(request, "network/index.html",{
            "currentUsername" : request.user.username, 
            "page_obj": paginator.get_page(request.GET.get('page')),
            "numpages_plus_one": paginator.num_pages+1,
            "likes": [post.id for post in usrCurrent.likes.all()] # Current user likes
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
        usrCurrent = User.objects.get(username=request.user.username) # Get current user object
        usrAll = User.objects.exclude(username=request.user.username) # Get users list, without current user
        # usrCurrent.follows is the list of people the user follows / usrCurrent.<Followers> is the list of people followinh the user
        numFollowers = usrCurrent.followers.all().count() # Get number of followers of current user <user_set>=<Followers>
        followed = usrCurrent.follows.all()
        numFollowed = followed.count() # Get number of users the current user follows
        posts = Post.objects.filter (author=usrCurrent).order_by(F('datetime').desc()) # Get posts of current user; first the recentest        
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


def following(request):
    usrCurrent = User.objects.get(username=request.user.username) # Get current user object
    following = usrCurrent.follows.all() # List of people the current user is following
    followingPosts = Post.objects.filter (author__in=following).order_by(F('datetime').desc()) # Get the posts from people user is following
    paginator = Paginator(followingPosts, CONST_linesPerPage) # Show CONST_linesPerPage lines per page.

    return render(request, "network/following.html",{
        "currentUsername" : request.user.username, 
        "page_obj": paginator.get_page(request.GET.get('page')),
        "numpages_plus_one": paginator.num_pages+1,
        "likes": [post.id for post in usrCurrent.likes.all()] # Current user likes
    })

def updatePost(request):
    if request.is_ajax and request.method == "POST":
        # Is an Ajax request and data comes in "request.body" not in "request.POST"!!!!
        data = json.loads(request.body)
        pid = data["id"]
        pcontent = data["contents"]
        try:
            Post.objects.filter(id=pid).update(content=pcontent)
            return JsonResponse({'message': f"Post saved successfully! {pid} & {pcontent}" })
        except KeyError:
            return JsonResponse({'message': "Key error!" })
    else:
        return render(request, "network/error.html", {"message": "Operation not allowed."})        

def likePost(request):
    if request.is_ajax and request.method == "POST":
        usrCurrent = User.objects.get(username=request.user.username) # Get current user object
        # Is an Ajax request and data comes in "request.body" not in "request.POST"!!!!
        data = json.loads(request.body)
        pid = data["id"]
        boolLike = data["like"]
        try:
            post = Post.objects.get(pk=pid) # Get the liked Post
        except KeyError:
            return JsonResponse({'message': "Key error!" })
        usrCurrent.likes.remove(post) # Remove that post from user likes   
        if boolLike: 
            usrCurrent.likes.add(post) # Add that post to user likes if clicked
       
        # Update total post likes
        post.totallikes = post.totallikes + (1 if boolLike else -1)
        post.save();
        return JsonResponse({
            'message': f"Like saved successfully! {pid} & {boolLike}",
            "totallikes": post.totallikes 
            })
    else:
        return render(request, "network/error.html", {"message": "Operation not allowed."})
