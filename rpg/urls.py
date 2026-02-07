# rpg/urls.py
from django.urls import path
from rpg.views import ProductListAPIView, ProductCreateAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),
]
