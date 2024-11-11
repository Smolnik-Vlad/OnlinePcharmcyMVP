from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated

from cart.permissions import IsCustomerOwner
from catalog.models import Product, Comments, Rating
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
        queryset = Comments.objects.filter(product_id=self.kwargs['product_id'])
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
