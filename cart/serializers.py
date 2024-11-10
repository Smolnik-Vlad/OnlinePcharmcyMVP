from django.db.models import F
from django.db.transaction import atomic
from rest_framework import serializers

from cart.models import Position, Cart
from catalog.models import Product
from catalog.serializers import ProductSerializer


class PositionSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        """
        Validate that the cart and product exist and that the requested amount is available.
        """

        cart_id = self.context.get("card_id")
        product = attrs.get("product_id")
        amount = attrs.get("amount")

        # Проверка существования корзины
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError("Cart does not exist.")

        # Проверка существования продукта
        try:
            product_instance = Product.objects.get(id=product)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")

        # Проверка доступного количества продукта
        if amount > product_instance.amount:
            raise serializers.ValidationError("Amount cannot exceed available stock.")

        return attrs

    @atomic
    def save(self, **kwargs):
        print(f"Kwargs: {self.validated_data} -- {self.context}")
        prod_id = self.validated_data.get('product_id')
        amount = self.validated_data.get('amount')
        cart_id = self.context.get("card_id")

        position = Position.objects.filter(
            product_id=prod_id,
            cart_id=cart_id,
        ).first()

        if position:
            position.amount += amount
            position.save(update_fields=['amount'])

        else:
            position = Position.objects.create(
                product_id=prod_id,
                amount=amount,
                cart_id=cart_id,
            )
        Product.objects.filter(id=prod_id).update(
            amount=F('amount') - amount,  # Decrease the amount in the 'Product' table
        )
        print(position.cart_id)
        return position

    class Meta:
        model = Position
        fields = ["id", "product_id", "amount"]
        # lookup_field = "product__id"


class CartSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True)
    numb_of_positions = serializers.IntegerField(read_only=True)
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "positions", "numb_of_positions", "total_price"]
        lookup_field = "product_id"
