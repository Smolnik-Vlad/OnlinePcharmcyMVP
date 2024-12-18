from django.contrib import admin

from catalog.models import Product, Rating


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "brand",
        "amount",
        "is_in_stock",
    )
    list_filter = (
        "brand",
        "price",
        "amount",
    )
    empty_value_display = "undefined"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "customer",
        "rating"
    )
