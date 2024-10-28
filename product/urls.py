from django.urls import path
from .views import CategoryListView, ProductListView

urlpatterns = [
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('products/<str:category_name>/', ProductListView.as_view(), name='product_list'),
]
