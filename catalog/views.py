from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.permissions import IsCustomerOwner
from catalog.get_tags_tool import key_words_extractor
from catalog.models import Product, Comment, Rating, Tag
from catalog.serializers import ProductSerializer, CommentSerializer, RatingSerializer


class CatalogListView(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = Product.in_stock.all()
    serializer_class = ProductSerializer

    search_fields = ("^title",)
    ordering_fields = ("price",)
    ordering = ("-addition_date",)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Used to add new positions to the cart, in case the user is a customer,
        and he is signed in.
        """
        return self.create(request, *args, **kwargs)


class CatalogRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin,
                                      generics.GenericAPIView):
    """
    View for retrieving one specific catalog item for observing;
    updating or deleting catalog items by administration.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@swagger_auto_schema(
    operation_description="Add a rating to position",
    request_body=RatingSerializer,
    responses={
        201: openapi.Response("Rating added successfully", RatingSerializer),
        400: "Amount exceeds available stock."
    }
)
class RatingCreateUpdate(mixins.CreateModelMixin,
                         generics.GenericAPIView):
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated, IsCustomerOwner)

    queryset = Rating.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Handles adding a new rating for a product.
        """
        res = self.create(request, *args, **kwargs)
        return res


class RatingGetByProduct(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = RatingSerializer

    lookup_field = ['product_id']

    def get_queryset(self):
        return Rating.objects.filter(product_id=self.kwargs['product_id'])

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentCreateList(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        generics.GenericAPIView):
    lookup_field = 'product_id'
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_id'] = self.kwargs['product_id']
        return context

    def get_queryset(self):
        queryset = Comment.objects.filter(product_id=self.kwargs['product_id'])
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Add a comment to position",
        request_body=CommentSerializer,
        responses={
            201: openapi.Response("Comment added successfully", CommentSerializer),
            400: "Amount exceeds available stock."
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Here is your request'),
        },
        required=['description']
    ),
    operation_description="Enter your request",
    responses={200: "Resource created successfully"}
)
@api_view(['POST'])
def search_product_by_description(request):
    try:
        description = request.data.get('description', None)
        if not description:
            return Response(
                {"error": "Name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        keywords = key_words_extractor.extract_keywords(description)
        print(f"{keywords=}")
        tags = Tag.objects.filter(title__in=keywords)
        print(f"{tags=}")
        products = Product.objects.filter(tags__in=tags) \
            .annotate(matching_tags=Count('tags')) \
            .order_by('-matching_tags')

        print(f"Prod: {products}")
        serialized_data = [{"addition_date": product.addition_date,
                            "amount": product.amount,
                            "average_rating": product.average_rating,
                            "barcode": product.barcode,
                            "brand": product.brand,
                            "expiration_date": product.expiration_date,
                            "id": product.id,
                            "info": product.info,
                            "is_in_stock": product.is_in_stock,
                            "price": product.price,
                            # "tags": product.tags,
                            "title": product.title,
                            "url": product.url
                            } for product in products]

        return Response(serialized_data)
    except Exception:
        return Response({})
