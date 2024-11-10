from rest_framework import mixins, generics

from catalog.models import Product
from catalog.serializers import SimpleProductSerializer


class CatalogListView(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = Product.in_stock.all()
    serializer_class = SimpleProductSerializer

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
    serializer_class = SimpleProductSerializer
    lookup_field = "id"

    # permission_classes = (
    #     IsStuffOrEmployeeOrReadOnly,
    # )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
