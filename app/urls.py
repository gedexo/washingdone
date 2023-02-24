from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path("add_product/<int:pk>/", views.add_product, name="add_product"),
    path("add_to_cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path(
        "add_single_to_cart/<int:pk>/",
        views.add_single_to_cart,
        name="add_single_to_cart",
    ),
    path("increase_qty/<int:pk>/", views.increase_qty, name="increase_qty"),
    path("decrease_qty/<int:pk>/", views.decrease_qty, name="decrease_qty"),
    path("delete_from_cart/<int:pk>/", views.delete_from_cart, name="delete_from_cart"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.success, name="success"),
    path("all_orders/", views.orders, name="orders"),
    path("products/", views.products, name="products"),
    path("product/<str:slug>/", views.product, name="product"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:slug>/", views.category, name="category"),
    path("search/results/", views.search, name="search"),
]
