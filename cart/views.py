from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics, response, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Position, Cart
from cart.permissions import IsCustomerOwner
from cart.serializers import PositionSerializer
from catalog.models import Rating
from catalog.serializers import RatingSerializer


# Create your views here.
class CartPositionView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    """
    View to manage cart positions for the authenticated user.
    Allows listing and creating positions in the user's cart.
    """
    serializer_class = PositionSerializer
    permission_classes = (IsCustomerOwner, IsAuthenticated)

    def get_queryset(self):
        # Получение позиций корзины, привязанных к текущему пользователю
        return Position.objects.filter(cart_id=self.request.user.customer.cart.id).select_related('product')

    def get_serializer_context(self):
        # Передача ID корзины в контексте сериализатора
        return {"card_id": self.request.user.customer.cart.id}

    @swagger_auto_schema(
        operation_description="Add a new position to the user's cart. Checks stock availability.",
        request_body=PositionSerializer,
        responses={
            201: openapi.Response("Position added successfully", PositionSerializer),
            400: "Amount exceeds available stock."
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Handles adding a new position to the cart.
        Checks the product's stock availability before adding.
        """
        res = self.create(request, *args, **kwargs)
        return res

    def get(self, request, *args, **kwargs):
        """
        Returns a list of positions for the user's cart.
        """
        return self.list(request, *args, **kwargs)


class CartPositionRetrieveUpdateDelete(mixins.RetrieveModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    permission_classes = (IsCustomerOwner, IsAuthenticated)
    lookup_field = ['position_id']

    serializer_class = PositionSerializer

    def get_object(self):
        # Получение позиции корзины по ID и привязанной к текущему пользователю
        position = Position.objects.filter(id=self.kwargs['position_id'], cart_id=self.request.user.customer.cart.id).first()

        if position is None:
            raise NotFound(detail="Position not found.")

        return position

    def get_serializer_context(self):
        # Передача ID корзины в контексте сериализатора
        return {"card_id": self.request.user.customer.cart.id}

    def get_queryset(self):
        # Получение позиций корзины, привязанных к текущему пользователю
        return Position.objects.filter(cart_id=self.request.user.customer.cart.id).select_related('product')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


