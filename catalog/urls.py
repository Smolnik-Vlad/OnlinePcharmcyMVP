from django.urls import path

from catalog.views import CatalogListView, CatalogRetrieveUpdateDeleteView

urlpatterns = [
    path('', CatalogListView.as_view()),  # endpoint to get list of customers
    path('<int:id>', CatalogRetrieveUpdateDeleteView.as_view())

]
