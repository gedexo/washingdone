from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("p/<str:slug>/", views.page, name="page"),
    path("blog/<str:slug>/", views.blog, name="blog"),
]
