from django.urls import path, include

from users.views import CustomerViewList, CustomerCreateView, CustomerRetrieveUpdateDeleteView

urlpatterns = [
    path('customers/', CustomerViewList.as_view()),  # endpoint to get list of customers
    path('new_customer/', CustomerCreateView.as_view()),  # endpoint to create a new one customer
    path('customer/<int:id>/', CustomerRetrieveUpdateDeleteView.as_view()),  # endpoint to update or delete customer

    path('auth/', include('djoser.urls.jwt')),

]
