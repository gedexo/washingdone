from __future__ import unicode_literals

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from tinymce.models import HTMLField
from versatileimagefield.fields import VersatileImageField

ORDER_STATUS = (
    ("not_yet_shipped", "Not Yet Shipped"),
    ("shipped", "Shipped"),
    ("cancelled", "Cancelled"),
    ("refunded", "Refunded"),
    ("delivered", "Delivered"),
)
STATE_CHOICES = (
    ("IN", "Out of India"),
    ("AN", "Andaman and Nicobar Islands"),
    ("AP", "Andhra Pradesh"),
    ("AR", "Arunachal Pradesh"),
    ("AS", "Assam"),
    ("BR", "Bihar"),
    ("CG", "Chandigarh"),
    ("CH", "Chhattisgarh"),
    ("DN", "Dadra and Nagar Haveli"),
    ("DD", "Daman and Diu"),
    ("DL", "Delhi"),
    ("GA", "Goa"),
    ("GJ", "Gujarat"),
    ("HR", "Haryana"),
    ("HP", "Himachal Pradesh"),
    ("JK", "Jammu and Kashmir"),
    ("JH", "Jharkhand"),
    ("KA", "Karnataka"),
    ("KL", "Kerala"),
    ("LA", "Ladakh"),
    ("LD", "Lakshadweep"),
    ("MP", "Madhya Pradesh"),
    ("MH", "Maharashtra"),
    ("MN", "Manipur"),
    ("ML", "Meghalaya"),
    ("MZ", "Mizoram"),
    ("NL", "Nagaland"),
    ("OR", "Odisha"),
    ("PY", "Puducherry"),
    ("PB", "Punjab"),
    ("RJ", "Rajasthan"),
    ("SK", "Sikkim"),
    ("TN", "Tamil Nadu"),
    ("TS", "Telangana"),
    ("TR", "Tripura"),
    ("UP", "Uttar Pradesh"),
    ("UK", "Uttarakhand"),
    ("WB", "West Bengal"),
)


class ProductCategory(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return str(self.title)


class Unit(models.Model):
    title = models.CharField(max_length=128)
    product = models.ForeignKey(
        "app.Product", on_delete=models.CASCADE, related_name="units"
    )
    price = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    mrp = models.DecimalField(
        default=0.0,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="MRP",
    )
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order",)
        verbose_name = "Product Unit"
        verbose_name_plural = "Product Units"

    def __str__(self):
        return str(self.title)

    @property
    def disc_percent(self):
        if self.mrp != 0:
            return round(((self.mrp - self.price) / self.mrp) * 100)
        else:
            return 0


class Product(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField()
    photo = VersatileImageField(upload_to="images/products")
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="products"
    )
    description = HTMLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    banner1 = VersatileImageField(upload_to="images/banners", blank=True, null=True)
    banner2 = VersatileImageField(upload_to="images/banners", blank=True, null=True)
    banner3 = VersatileImageField(upload_to="images/banners", blank=True, null=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return str(self.title)

    @property
    def price(self):
        return self.units.first().price

    @property
    def mrp(self):
        return self.units.first().mrp


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class OrderItem(models.Model):
    user_session = models.CharField(max_length=100)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.DecimalField(default=1, decimal_places=0, max_digits=15)
    is_placed = models.BooleanField(default=False)

    def __str__(self):
        subtotal = self.quantity * self.unit.product.price
        return f"{self.quantity} of ({self.unit.product.title}) total {subtotal}"

    @property
    def product_price(self):
        return self.unit.product.price

    @property
    def subtotal(self):
        return self.quantity * self.unit.product.price


class Order(models.Model):
    user_session = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    items = models.ManyToManyField(OrderItem)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default="KL")
    notes = models.TextField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100, choices=ORDER_STATUS, default="not_yet_shipped"
    )

    class Meta:
        ordering = ("-order_date", "status")

    def __str__(self):
        return self.order_id

    @property
    def total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.subtotal()
        return total
