import json

from app.models import Product, ProductCategory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import ContactForm
from .models import Banner, Blog, Client, Deal, Page, Testimonial


def index(request):
    categories = ProductCategory.objects.filter(is_active=True)
    banners = Banner.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    blogs = Blog.objects.filter(is_active=True)
    clients = Client.objects.filter()
    deals = Deal.objects.filter(is_active=True)
    context = {
        "is_index": True,
        "banners": banners,
        "categories": categories,
        "clients": clients,
        "products": products,
        "testimonials": testimonials,
        "blogs": blogs,
        "deals": deals,
    }
    return render(request, "web/index.html", context)


def about(request):
    context = {"is_about": True}
    return render(request, "web/about.html", context)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully updated",
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
        context = {
            "is_contact": True,
            "form": form,
        }
    return render(request, "web/contact.html", context)


def blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    context = {
        "blog": blog,
    }
    return render(request, "web/blog.html", context)


def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    context = {
        "page": page,
    }
    return render(request, "web/page.html", context)
