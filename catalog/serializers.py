from random import choices

from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from catalog.models import Product, Rating, Comment, Tag
from catalog.check_comment_tool import check_comment_tool
from users.models import Customer


class ProductSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.BooleanField(read_only=True)
    url = serializers.URLField(read_only=True)
    price = serializers.FloatField()
    average_rating = serializers.SerializerMethodField()
    tags = serializers.ListSerializer(child=serializers.CharField(), allow_empty=True)

    def get_average_rating(self, obj):
        """
        Метод для извлечения среднего рейтинга продукта.
        """
        return obj.average_rating

    class Meta:
        fields = '__all__'
        model = Product
        lookup_field = 'id'
        extra_kwargs = {
            "url": {
                "lookup_field": "id"
            }
        }

    def save(self, **kwargs):
        list_of_tags_str = self.validated_data.pop('tags', [])
        product: Product = super(ProductSerializer, self).save(**kwargs)
        print(list_of_tags_str)
        for tag_str in list_of_tags_str:
            current_tag, created = Tag.objects.get_or_create(
                title=tag_str,
                defaults={
                    'title': tag_str
                }
            )
            current_tag.product.add(product)
        product.tags.set(Tag.objects.filter(product=product))

        return product


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.ChoiceField(choices=Rating.RATING_CHOICES)
    product_id = serializers.IntegerField()
    customer_email = serializers.ReadOnlyField(source='customer.user.email')

    class Meta:
        fields = ('rating', 'product_id', 'customer_email')
        model = Rating
        lookup_field = 'id'

    def validate(self, attrs):
        product_id = attrs.get('product_id')
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Product does not exist.")
        return attrs

    def save(self, **kwargs):
        product_id = self.validated_data.get('product_id')
        customer: Customer = self.context['request'].user.customer
        rating = self.validated_data.get('rating')

        # Check if customer has already rated the product
        rating_obj: Rating = Rating.objects.filter(
            product_id=product_id,
            customer=customer
        ).first()
        if rating_obj:
            rating_obj.rating = rating
            rating_obj.save(update_fields=['rating'])
        else:
            rating_obj = Rating.objects.create(
                product_id=product_id,
                customer=customer,
                rating=rating
            )

        return rating_obj


class CommentSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(read_only=True)
    comment_field = serializers.CharField()
    customer_email = serializers.ReadOnlyField(source='customer.user.email')

    class Meta:
        model = Comment
        fields = ('product_id', 'customer_email', 'comment_field', 'changed_at', 'id')
        read_only_fields = ['changed_at', 'product_id', 'id', 'customer_email']

    def validate(self, attrs):
        product_id = self.context.get('product_id')
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Product does not exist.")
        attrs['product_id'] = product_id
        return attrs

    def validate_comment_field(self, value):
        if check_comment_tool.check_toxicity(value):
            raise serializers.ValidationError("Comment field contains inappropriate content.")
        return value

    def save(self, **kwargs):
        self.validated_data["customer"] = self.context['request'].user.customer
        print(f"Validated data: {self.validated_data}")
        return super().save(**kwargs)
