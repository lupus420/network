
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("get_posts", views.get_posts, name="get_posts"),
    path("get_post", views.get_post, name="get_post"),
    path("pages_count", views.pages_count, name="pages_count"),
    path("get_logged_user", views.get_logged_user, name="get_logged_user"),
    path("like_post", views.like_post, name="like_post"),
    path("make_post", views.make_post, name="make_post"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("get_comments", views.get_comments, name="get_comments"),
    path("make_comment", views.make_comment, name="make_comment"),
]
