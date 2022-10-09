
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user_profile/<int:user_id>/", views.user_profile, name="user_profile"),
    path("user_profile/<int:user_id>/following/add", views.follow, name="follow"),
    path("user_profile/<int:user_id>/following/remove", views.unfollow, name="unfollow"),
    path("user_profile/<int:user_id>/following_list", views.following_list, name='following_list'),


    path("comment/<int:posts_id>/", views.comment, name="comment"),
    path("vote_rating/<int:posts_id>/", views.vote_rating, name="vote_rating"), 

    


    # API Routes
    path("comments", views.comment_api, name="comments"),
]
 