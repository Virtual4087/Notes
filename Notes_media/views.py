from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import IntegrityError
from .models import User, Post, Image
from django.contrib.auth import login, logout, authenticate
import magic


# Create your views here.
def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.FILES["image"]
        file = request.FILES["pdf_file"]
        if file:
            mime = magic.Magic()
            file_type = mime.from_buffer(file.read())

            if not "PDF" in file_type:
                return render(
                    request,
                    "index.html",
                    {
                        "message": "You can only upload a pdf file!",
                        "posts": Post.objects.all(),
                    },
                )
        try:
            post_image = Image.objects.create(image=image)
            post_image.save()
            post = Post.objects.create(
                user=request.user, title=title, description=description, file=file
            )
            post.save()
            post.image.add(post_image)
            return redirect("index")

        except:
            return render(
                request,
                "index.html",
                {
                    "message": "An error occurred. Couldn't post!",
                    "posts": Post.objects.all(),
                },
            )

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
