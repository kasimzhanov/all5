from django.urls import path
from rpg.views import ProductListAPIView, ProductCreateAPIView
from .views import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),

    
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
]