from django.urls import path

from cart.views import CartPositionView, CartPositionRetrieveUpdateDelete

urlpatterns = [
    # path('<int:id>/edit/', CartListUpdateCreatePositionsView.as_view()),  # endpoint to get list of customers
    path('<int:position_id>/', CartPositionRetrieveUpdateDelete.as_view()),
    path('', CartPositionView.as_view()),

]
