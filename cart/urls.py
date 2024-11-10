from django.urls import path

from cart.views import CartPositionView, CartPositionRetrieveUpdateDelete, RatingGetByProduct

urlpatterns = [
    # path('<int:id>/edit/', CartListUpdateCreatePositionsView.as_view()),  # endpoint to get list of customers
    path('<int:id>/', CartPositionRetrieveUpdateDelete.as_view()),
    path('', CartPositionView.as_view()),

]
