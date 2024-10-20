from rest_framework import serializers

from goods.models import Category, Products


class ProductsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["created"]


# class ProductsSerializers(serializers.serializerserializer):
#     class Meta:
#         model = Products
#         # fields = "__all__"
#         fields = ("id", "name", "price", "category")
