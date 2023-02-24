from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from tinymce.models import HTMLField
from versatileimagefield.fields import VersatileImageField


class About(models.Model):
    summary = models.TextField()
    description = HTMLField()
    address = models.TextField()
    email = models.EmailField(max_length=128, default="info@washingdone.com")
    phone = models.CharField(max_length=128, default="+91 9876 543 210")
    brochure = models.FileField(blank=True, null=True, upload_to="files/brochure")
    working_hours = models.CharField(
        max_length=128, default="Mon – Sat : 9:00 am – 7:00 pm"
    )

    class Meta:
        verbose_name = "About Washingdone"
        verbose_name_plural = "About Washingdone"

    def clean(self):
        if About.objects.count() >= 1 and self.pk is None:
            raise ValidationError(
                "You can only create one About. Try editing/removing one of the existing about."
            )

    def __str__(self):
        return str("Change About Washingdone")


class Banner(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128)
    photo = VersatileImageField(upload_to="images/banners", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    icon = models.TextField()

    def __str__(self):
        return str(self.title)


class Category(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Blog(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="categories"
    )
    date = models.DateField(auto_now_add=True)
    photo = VersatileImageField(upload_to="images/blogs", blank=True, null=True)
    summary = models.TextField()
    content = HTMLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return str(self.title)


class Deal(models.Model):
    product = models.ForeignKey(
        "app.Product", on_delete=models.CASCADE, related_name="product"
    )
    available_upto = models.DateTimeField()
    special_price = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-available_upto",)

    def __str__(self):
        return str(self.product.title)


class Page(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = HTMLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-title",)

    def __str__(self):
        return str(self.title)


class Client(models.Model):
    name = models.CharField(max_length=128)
    photo = VersatileImageField(upload_to="images/testimonials")

    def __str__(self):
        return str(self.name)


class Testimonial(models.Model):
    name = models.CharField(max_length=128)
    photo = VersatileImageField(upload_to="images/testimonials")
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return str(self.name)


class Social(models.Model):
    order = models.IntegerField(unique=True)
    media = models.CharField(max_length=100)
    link = models.URLField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order",)
        verbose_name = "Social Media"
        verbose_name_plural = "Social Medias"

    def __str__(self):
        return str(self.media)


class Contact(models.Model):
    name = models.CharField(max_length=120)
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=120, blank=True, null=True)
    place = models.CharField(max_length=120, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return str(self.name)
