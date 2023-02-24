from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Order, OrderItem, Product, ProductCategory, Review, Unit


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class UnitResource(resources.ModelResource):
    class Meta:
        model = Unit


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "is_active")
    autocomplete_fields = ("category",)
    search_fields = ("title",)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)


@admin.register(Unit)
class UnitAdmin(ImportExportModelAdmin):
    resource_class = UnitResource
    autocomplete_fields = ("product",)
    list_display = ("title", "product", "price", "mrp", "order", "is_active")
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ("product",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ("__str__",)
    readonly_fields = ("user_session",)
    list_display = ("__str__", "user_session")
    autocomplete_fields = ("unit",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ("items",)


admin.site.site_header = "WashingDone Administration"
admin.site.site_title = "WashingDone Admin Portal"
admin.site.index_title = "Welcome to WashingDone Admin Portal"
