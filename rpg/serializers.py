from rest_framework import serializers
from .models import Category, Model, ProductModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = [
            'id',
            'title',
            'price',
            'category',
            'model',
            'created_at',
            'image',
        ]