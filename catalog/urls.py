from django.urls import path

from catalog.views import CatalogListView, CatalogRetrieveUpdateDeleteView, CommentCreateList, RatingCreateUpdate, \
    RatingGetByProduct, search_product_by_description

urlpatterns = [
    path('', CatalogListView.as_view()),  # endpoint to get list of customers
    path('<int:id>', CatalogRetrieveUpdateDeleteView.as_view()),
    path('rating/', RatingCreateUpdate.as_view()),
    path('rating/<int:product_id>', RatingGetByProduct.as_view()),
    path('comment/<int:product_id>', CommentCreateList.as_view()),
    path('search_product_by_description/', search_product_by_description, name='search_product_by_description')
]
