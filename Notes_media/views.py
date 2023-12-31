from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db import IntegrityError
from .models import User, Post, Image, Comment, Category, Level
from django.contrib.auth import login, logout, authenticate
import magic
from django.contrib import messages
import json
from django.db.models import Q, Count
import os
from django.conf import settings

def index(request: HttpRequest):
    return render(
        request, "index.html", {"posts": Post.objects.all().order_by("-date")}
    )


def search(request: HttpRequest):
    posts = None
    parameters = request.GET
    if "sort" in parameters:
        sortby = parameters["sort"]
        if sortby == "saved" and request.user.is_authenticated:
            posts = request.user.saved_post.all()
        elif sortby == "new":
            posts = Post.objects.all().order_by("-date")
        elif sortby == "top":
            posts = Post.objects.annotate(num_likes=Count("like")).order_by(
                "-num_likes"
            )
        elif sortby == "following" and request.user.is_authenticated:
            posts = Post.objects.filter(user__in=request.user.following.all())
        elif sortby == "old":
            posts = Post.objects.all().order_by("date")
    elif "search" in parameters:
        search = parameters["search"]
        posts = Post.objects.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        ).order_by("-date")
    elif "category" in parameters:
        try:
            category = parameters["category"]
            posts = Post.objects.filter(
                category=Category.objects.get(category=category)
            ).order_by("-date")
        except:
            pass
    elif "level" in parameters:
        try:
            level = parameters["level"]
            posts = Post.objects.filter(level=Level.objects.get(level=level)).order_by(
                "-date"
            )
        except:
            pass

    return render(request, "index.html", {"posts": posts})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request, "register.html", {"message": "Passwords don't match!"}
            )

        for user in User.objects.all():
            if email == user.email:
                return render(
                    request,
                    "register.html",
                    {"message": "This email is already in use."},
                )

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect("index")
        except Exception as e:
            return render(
                request, "register.html", {"message": str(e)}
            )
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "login.html", {"message": "Invalid username and/or password."}
            )
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "GET":
        return render(request, "post.html", {"post": post})

    elif request.method == "POST":
        source = request.headers.get("Source")
        if source == "like_unlike":
            try:
                data = json.loads(request.body.decode("utf-8"))
                if data.get("perform") == "unlike":
                    post.like.remove(request.user)
                else:
                    post.like.add(request.user)
                return JsonResponse({"success": True})
            except:
                return JsonResponse({"success": False})

        elif source == "post_comment":
            try:
                data = request.body.decode("utf-8")
                comment = Comment.objects.create(
                    user=request.user, post=post, comment=data
                )
                comment.save()
                return JsonResponse({"success": True})
            except:
                return JsonResponse({"success": False})

        elif source == "save_post":
            try:
                data = json.loads(request.body.decode("utf-8"))
                if data["perform"] == "save":
                    request.user.saved_post.add(post)
                else:
                    request.user.saved_post.remove(post)
                return JsonResponse({"success": True})
            except:
                return JsonResponse({"success": False})

    elif request.method == "DELETE":
        try:
            if post.user == request.user:
                for image in post.image.all():
                    image.image.delete()
                post.file.delete()
                post.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False})
        except:
            return JsonResponse({"success": False})


def createpost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"].strip()
            description = request.POST["description"].strip()
            category = request.POST["category"]
            level = request.POST["level"]

            try:
                post = Post.objects.create(
                    user=request.user,
                    title=title,
                    description=description,
                    category=Category.objects.get(category=category),
                    level=Level.objects.get(level=level),
                )
                post.save()

            except:
                messages.error(request, "An error occurred. Couldn't post!")
                return redirect("create")

            if "pdf_file" in request.FILES:
                file = request.FILES["pdf_file"]
                mime = magic.Magic()
                file_type = mime.from_buffer(file.read())

                if "PDF" in file_type:
                    post.file = file
                    post.save()

                else:
                    post.delete()
                    messages.error(request, "Error while uploading pdf file!")
                    return redirect("create")

            if "image" in request.FILES:
                images = request.FILES.getlist("image")
                for image in images:
                    mime = magic.Magic()
                    file_type = mime.from_buffer(image.read())
                    if not "image" in file_type:
                        post.delete()
                        messages.error(request, "Error while uploading image!")
                        return redirect("create")

                    try:
                        post_image = Image.objects.create(image=image)
                        post_image.save()
                        post.image.add(post_image)
                    except:
                        post.delete()
                        messages.error(request, "Error while uploading image!")
                        return redirect("create")
            return redirect("index")
        return render(
            request,
            "create-post.html",
            {"categories": Category.objects.all(), "levels": Level.objects.all()},
        )
    else:
        return redirect("index")


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    if request.method == "POST":
        source = request.headers.get("Source")
        if source == "follow_unfollow":
            try:
                data = json.loads(request.body.decode("utf-8"))
                if data.get("perform") == "follow":
                    request.user.following.add(user)
                else:
                    request.user.following.remove(user)
                return JsonResponse({"success": True})
            except:
                return JsonResponse({"success": False})

        elif source == "change_pp":
            if request.user != user:
                return JsonResponse({"success": False})
            try:
                image = request.FILES.get("file")
                mime = magic.Magic()
                file_type = mime.from_buffer(image.read())
                if not "image" in file_type:
                    return JsonResponse({"success": False})
                
                file_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_picture.file))

                user.profile_picture = image
                user.save()

                if os.path.exists(file_path):
                    if not "\default_images\\" in str(file_path):
                        os.remove(file_path)

                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse({"success": False, "exception": str(e)})

    elif request.method == "PUT":
        if request.user != user:
            return JsonResponse({"success": False})
        
        source = request.headers.get("Source")

        if source == "edit_about":
            data = request.body.decode("utf-8")
            try:
                user.about = data
                user.save()
                return JsonResponse({"success": True})
            except:
                return JsonResponse({"success": False})
            
        elif source == "edit_info":
            data = json.loads(request.body.decode("utf-8"))
            try:
                user.full_name = data["fullname"]
                user.level = Level.objects.get(level=data["level"])
                if data["birthday"]:
                    user.birthday = data["birthday"]
                user.location = data["location"]
                user.save()
                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse({"success": False, "error" : str(e)})
            
    return render(request, "profile.html", {"profile": user, "categories": Category.objects.all(), "levels": Level.objects.all()})
