from django.forms import model_to_dict
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from goods.models import Category, Products

from goods.serializers import CategorySerializers, ProductsSerializers
from permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Category.objects.all()[:3]
        return Category.objects.filter(pk=pk)

    @action(methods=["get"], detail=True)
    def category(self, request, pk=None):
        # это когда список detail=False адрес http://127.0.0.1:8000/api/v1/category/category/
        # cats = Category.objects.all()
        # return Response({"cats": [c.name for c in cats]})

        # Это когда нужно конкретную запись detail=True, pk=None адрес http://127.0.0.1:8000/api/v1/category/pk/category/
        cats = Category.objects.get(pk=pk)
        return Response({"cats": cats.name})


# class CategoryViewSet(
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.ListModelMixin,
#     GenericViewSet,
# ):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializers


# class ProductListAPIView(generics.ListCreateAPIView):
#     queryset = Products.objects.all().values()[:10]
#     serializer_class = ProductsSerializers
#
#
# class ProductAPIUpdate(generics.UpdateAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductsSerializers
#
#
class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )


class CategoryAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (IsOwnerOrReadOnly,)


class CategoryAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (IsAdminOrReadOnly,)


#
#
# class CategoryAPIUDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializers


# class CatalogViewSet(APIView):
#     def get(self, request):
#         lst = Products.objects.all().values()[:1000]
#         return Response({"title": list(lst)})
#
#     def post(self, request):
#         # пример запроса для другой таблицы.
#         post_new = Products.objects.create(
#             title=request.data["title"],
#             content=request.data["content"],
#             category=request.data["category"],
#         )
#         return Response({"post": model_to_dict(post_new)})


# class CatalogViewSet(ListAPIView):
#
#     # queryset = Products.objects.filter(category=8162).select_related(
#     #     "category", "brand"
#     # )
#     queryset = Products.objects.all()[:1000]
#     serializer_class = ProductsSerializers
