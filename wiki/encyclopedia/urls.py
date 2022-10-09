from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entries, name="entry"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("create/", views.create, name="create"),
    path("random/", views.random, name="random"),
    path("search/", views.search, name="search"),


]
