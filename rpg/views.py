from rest_framework import generics, filters
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Category, Model, ProductModel
from .serializers import (
    CategorySerializer,
    ModelSerializer,
    ProductSerializer
)


class ProductListAPIView(generics.ListAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.query_params.get('category')
        model = self.request.query_params.get('model')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if category:
            queryset = queryset.filter(category_id=category)

        if model:
            queryset = queryset.filter(model_id=model)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class ModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer