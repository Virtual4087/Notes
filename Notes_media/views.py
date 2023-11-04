from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import IntegrityError
from .models import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message" : "Passwords don't match!"
            })
        
        for user in User.objects.all():
            if email == user.email:
                return render(request, "register.html", {
                    "message" : "This email is already in use."
                })

        try:
            user = User.objects.create(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect("index")
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken!"
            })
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username, password=password)

        except User.DoesNotExist:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("index")