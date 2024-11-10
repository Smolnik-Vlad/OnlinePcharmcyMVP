from rest_framework import serializers

from catalog.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.BooleanField(read_only=True)
    url = serializers.URLField(read_only=True)
    price = serializers.FloatField()

    class Meta:
        fields = '__all__'
        model = Product
        lookup_field = 'id'
        extra_kwargs = {
            "url": {
                "lookup_field": "id"
            }
        }
