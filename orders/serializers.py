from rest_framework import serializers
from orders.models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Product
		fields = ('id', 'name', 'description')

class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = ('id', 'name')