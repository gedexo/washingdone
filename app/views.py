from __future__ import unicode_literals

import json

from app.decorators import secure_checkout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import OrderForm, OrderItemForm, ReviewForm
from .functions import id_generator
from .models import Order, OrderItem, Product, Review, Unit


def search(request):
    dataset = Product.objects.filter(is_active=True)
    new_dataset = Product.objects.none()
    query = request.GET.get("q")
    if query:
        new_dataset = dataset.filter(
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(description__icontains=query)
        )
    print(new_dataset)
    context = {
        "is_search": True,
        "instance": new_dataset,
    }
    return render(request, "web/search.html", context)


def categories(request):
    instances = Category.objects.filter(is_active=True)
    context = {
        "is_categories": True,
        "instances": instances,
    }
    return render(request, "web/categories.html", context)


def category(request, slug):
    instance = get_object_or_404(Category, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=instance.category, is_active=True
    )
    add_to_cart_form = OrderItemForm()
    context = {
        "instance": instance,
        "related_products": related_products,
        "add_to_cart_form": add_to_cart_form,
    }
    return render(request, "web/category.html", context)


def products(request):
    instances = Product.objects.filter(is_active=True)
    context = {
        "is_products": True,
        "instances": instances,
    }
    return render(request, "web/products.html", context)


def product(request, slug):
    instance = get_object_or_404(Product, slug=slug, is_active=True)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.product = instance
            data.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Your review will be visible after moderation",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )
    else:
        related_products = Product.objects.filter(
            category=instance.category, is_active=True
        )
        reviews = Review.objects.filter(
            product=instance, is_approved=True, is_active=True
        )
        reviews_count = reviews.count()
        form = ReviewForm()
        add_to_cart_form = OrderItemForm()
        add_to_cart_form.fields["unit"].queryset = Unit.objects.filter(product=instance)
        context = {
            "instance": instance,
            "reviews": reviews,
            "reviews_count": reviews_count,
            "related_products": related_products,
            "add_to_cart_form": add_to_cart_form,
            "form": form,
        }
        return render(request, "web/product_details.html", context)


def add_product(request, pk):
    user_session = request.session.session_key
    unit = Unit.objects.filter(product=pk, is_active=True).first()

    if OrderItem.objects.filter(
        user_session=user_session, unit=unit, is_placed=False
    ).exists():
        quantity = 1
        order_item = OrderItem.objects.get(
            user_session=user_session, unit=unit, is_placed=False
        )
        order_item.quantity += quantity
        order_item.save()
        response_data = {
            "status": "true",
            "title": "Product Added",
            "message": "Cart Successfully Updated.",
        }
    else:
        OrderItem(
            user_session=user_session,
            unit=unit,
            quantity=1,
        ).save()
        response_data = {
            "status": "true",
            "title": "Product Updated",
            "message": "Cart Successfully Updated.",
        }
    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )


def add_to_cart(request, pk):
    user_session = request.session.session_key
    unit = Unit.objects.filter(product=pk, is_active=True).first()
    form = OrderItemForm(request.POST)
    if not OrderItem.objects.filter(
        user_session=user_session, unit=unit, is_placed=False
    ).exists():
        if form.is_valid():
            data = form.save(commit=False)
            data.user_session = user_session
            data.unit = unit
            data.quantity = form.cleaned_data["quantity"]
            data.save()
            response_data = {
                "status": "true",
                "title": "Product Added",
                "message": "Cart Successfully Updated.",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )
    else:
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            order_item = OrderItem.objects.get(
                user_session=user_session, unit=unit, is_placed=False
            )
            order_item.quantity += quantity
            order_item.save()
            response_data = {
                "status": "true",
                "title": "Product Updated",
                "message": "Cart Successfully Updated.",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )


def add_single_to_cart(request, pk):
    user_session = request.session.session_key
    unit = Unit.objects.filter(product=pk, is_active=True).first()
    OrderItemForm(request.POST)
    if not OrderItem.objects.filter(
        user_session=user_session, unit=unit, is_placed=False
    ).exists():
        OrderItem(user_session=user_session, unit=unit, quantity=1).save()
        response_data = {
            "status": "true",
            "title": "Product Added",
            "message": "Cart Successfully Updated.",
        }
    else:
        order_item = OrderItem.objects.get(
            user_session=user_session, unit=unit, is_placed=False
        )
        order_item.quantity += 1
        order_item.save()
        response_data = {
            "status": "true",
            "title": "Product Updated",
            "message": "Cart Successfully Updated.",
        }
    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )


def delete_from_cart(request, pk):
    OrderItem.objects.filter(pk=pk, is_placed=False).delete()
    response_data = {
        "status": "true",
        "reload": "true",
        "title": "Order Item Deleted",
        "message": "Order Item Deleted and Cart Updated successfully.",
    }
    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )


def cart(request):
    context = {}
    return render(request, "web/cart.html", context)


@secure_checkout
def checkout(request):
    user_session = request.session.session_key
    order_item = OrderItem.objects.filter(user_session=user_session, is_placed=False)
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_session = user_session
            data.order_id = id_generator()
            data.save()
            for i in order_item:
                data.items.add(i)
            order_item.update(is_placed=True)

            response_data = {
                "status": "true",
                "title": "Success",
                "message": "Your Order successfully placed",
                "redirect": "true",
                "redirect_url": reverse("app:success"),
            }
        else:
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )
    else:
        form = OrderForm()
        context = {
            "form": form,
        }
        return render(request, "web/checkout.html", context)


def success(request):
    context = {
        "orders": Order.objects.filter(user_session=request.session.session_key),
    }
    return render(request, "web/success.html", context)


@login_required
def orders(request):
    context = {
        "orders": Order.objects.all(),
    }
    return render(request, "web/orders.html", context)


def increase_qty(request, pk):
    order_item = OrderItem.objects.get(pk=pk)
    order_item.quantity += 1
    order_item.save()
    response_data = {
        "status": "true",
        "reload": "true",
        "title": "Order Item Updated",
        "message": "Order Item Updated.",
    }
    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )


def decrease_qty(request, pk):
    order_item = OrderItem.objects.get(pk=pk)
    order_item.quantity -= 1
    order_item.save()
    response_data = {
        "status": "true",
        "reload": "true",
        "title": "Order Item Updated",
        "message": "Order Item Updated.",
    }
    return HttpResponse(
        json.dumps(response_data), content_type="application/javascript"
    )
