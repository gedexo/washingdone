import datetime

from app.models import OrderItem
from django.db.models import F, Sum
from web.models import About, Page

from .models import Social


def main_context(request):
    datetime.date.today()
    pages = Page.objects.filter(is_active=True)
    user_session = request.session.session_key
    order_items = OrderItem.objects.filter(user_session=user_session, is_placed=False)
    if order_items:
        session_user_total = order_items.aggregate(
            total=Sum(F("unit__price") * F("quantity"))
        )["total"]
    else:
        session_user_total = 0

    if not request.session.session_key:
        request.session.create()

    return {
        "domain": request.META["HTTP_HOST"],
        "socials": Social.objects.all(),
        "about": About.objects.last(),
        "pages": pages,
        "order_items": order_items,
        "session_user_total": session_user_total,
    }
