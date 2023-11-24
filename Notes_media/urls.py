from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("post/<int:post_id>", views.post, name="post"),
    path("create-post", views.createpost, name="create"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("search", views.search, name="search"),
]
