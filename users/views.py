from django.contrib.admin.utils import lookup_field
from django.shortcuts import render
from rest_framework import mixins, generics

from users.models import Customer
from users.serializers import CustomerSerializer


# Create your views here.
class CustomerViewList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # permission_classes = [IsStaff]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class CustomerCreateView(mixins.RetrieveModelMixin, generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [permissions.AllowAny]


class CustomerRetrieveUpdateDeleteView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    queryset = Customer.objects.all()
    lookup_field = 'id'
    serializer_class = CustomerSerializer
    # permission_classes = [IsStaffOrOwner]

    def get(self, request, *args, **kwargs):
        print(kwargs)
        print(lookup_field)
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)