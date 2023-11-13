from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from .models import User, Post, Image
from django.contrib.auth import login, logout, authenticate
import magic
from django.contrib import messages
import json

def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]

        try:
            post = Post.objects.create(
                user=request.user, title=title, description=description
            )
            post.save()

        except:
            messages.error(request, "An error occurred. Couldn't post!")
            return redirect("index")
        
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
                return redirect("index")

        if "image" in request.FILES:
            image = request.FILES["image"]
            mime = magic.Magic()
            file_type = mime.from_buffer(image.read())
            if not "image" in file_type:
                post.delete()
                messages.error(request, "Error while uploading image!")
                return redirect("index")
            
            try:
                post_image = Image.objects.create(image=image)
                post_image.save()
                post.image.add(post_image)
            except:
                post.delete()
                messages.error(request, "Error while uploading image!")
                return redirect("index")
        return redirect("index")

    return render(request, "index.html", {"posts": Post.objects.all()})


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
        except IntegrityError:
            return render(
                request, "register.html", {"message": "Username already taken!"}
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

def edit(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=post_id)
            data = json.loads(request.body.decode('utf-8'))
            if data.get("perform") == "unlike":
                post.like.remove(request.user)
            else:
                post.like.add(request.user)
            return JsonResponse({"success" : True})
        except:
            return JsonResponse({"success" : False})
    
    elif request.method == "DELETE":
        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                for image in post.image.all():
                    image.image.delete()
                post.file.delete()
                post.delete()
                return JsonResponse({"success" : True})
            else:
                return JsonResponse({"success" : False})
        except:
            return JsonResponse({"success" : False})


# def profile(request, user_id):

#     return redirect("profile")
