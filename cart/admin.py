from django.contrib import admin

from cart.models import Position, Cart


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'numb_of_positions', 'total_price')


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'amount', 'price')
    list_filter = ('product', 'amount')
    list_editable = ('amount',)
    search_fields = ('amount',)


admin.site.register(Position, PositionAdmin)
admin.site.register(Cart, CartAdmin)