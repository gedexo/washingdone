from app.models import OrderItem
from django.db.models import Count
from django.shortcuts import render


def ajax_required(function):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return render(request, "error/400.html", {})
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def secure_checkout(function):
    def wrap(request, *args, **kwargs):
        duplicate_cart_items = (
            OrderItem.objects.filter(
                user_session=request.session.session_key, is_placed=False
            )
            .values(
                "unit",
            )
            .annotate(Count("unit"))
            .order_by()
            .filter(unit__count__gt=1)
        )
        if duplicate_cart_items:
            context = {
                "code": "Error",
                "message": "An error occured. Please clear your cart and try again",
            }
            return render(request, "error/custom.html", context)

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
