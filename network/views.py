from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from json import loads
# from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post, Comment, Follow

POSTS_PER_PAGE = 4

def index(request):
    return render(request, "network/index.html")


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
    

def make_post(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            post_content = body.get("post_content")
            author = request.user
            post = Post.objects.create(body=post_content, author=author)
            print("post saved")
            return JsonResponse(post.serialize())
        except:
            return JsonResponse({"error": "Post not saved."}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def get_paginator():
    """
    return paginator with all posts sorted by newest first
    """
    all_posts = Post.objects.all()
    #reverse order of posts so there is newest first
    all_posts = all_posts[::-1]
    paginator = Paginator(all_posts, POSTS_PER_PAGE)
    return paginator


def get_posts(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    paginator = get_paginator()
    posts = paginator.get_page(page)
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)
    else:
        return JsonResponse({"error": "GET request required."}, status=400)

def get_post(request):
    try:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(id = post_id)
        return JsonResponse(post.serialize())
    except:
        return JsonResponse({"error": "Bad request."}, status=400)

def get_logged_user(request):
    if request.user.is_authenticated:
        return JsonResponse(request.user.serialize())
    else:
        return JsonResponse({"error": "User not logged in."}, status=400)


def pages_count(request):
    if request.method == "GET":
        paginator = get_paginator()
        pages_counter = paginator.num_pages
        return JsonResponse({"pages_counter": pages_counter}, safe=False)
    else:
        return JsonResponse({"error": "GET request required."}, status=400) 


def like_post(request):
    '''
    Like or unlike a post.
    '''
    if request.method == "POST":
        try:
            # get python dictionary from json
            data = json.loads(request.body)
            post_id = data.get("post_id")
            user_id = data.get("user_id")
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=user_id)
            if user in post.likes.all():
                post.likes.remove(user)
                return JsonResponse({"message": "unliked"})
            else:
                post.likes.add(user)
                return JsonResponse({"message": "liked"})
        except:
            return JsonResponse({"error": "Invalid interaction with like button"}, status=400)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def follow(request):
    '''
    Follow or unfollow a user.
    '''
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            follow_from = data.get("follow_from")
            follow_to = data.get("follow_to")
            follow_from_user = User.objects.get(id=follow_from)
            follow_to_user = User.objects.get(id=follow_to)
            if follow_to_user in follow_from_user.following.all():
                follow_from_user.following.remove(follow_to_user)
                return JsonResponse({"message": "unfollowed"})
            else:
                follow_from_user.following.add(follow_to_user)
                return JsonResponse({"message": "followed"})
        except:
            return JsonResponse({"error": "Invalid interaction with follow button"}, status=400)
    else:
        JsonResponse({"error": "POST request required."}, status=400)


#to get to this view user must be logged in
@login_required
def following(request):
    try:
        # get all follows where logged in user is the follower
        all_follows = request.user.following.all()
        all_followed_by = request.user.followed_by.all()
        return render(request, "network/following.html",{
            "all_follows": all_follows,
            "all_followed_by": all_followed_by,
        })
    except:
        return render(request, "network/following.html",{
            "error": "Bad request."
        })
    

def profile(request, username):
    try:
        user = User.objects.get(username=username)
        return render(request, "network/profile.html", {
            "user": user,
        })
    except:
        return render(request, "network/profile.html", {
            "error": "There is no such profile.",
        })