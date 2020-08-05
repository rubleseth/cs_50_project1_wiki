from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new", views.new, name="new"),
    path("search/", views.search, name="search"),
    path("wiki/", views.random_page, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),

]
