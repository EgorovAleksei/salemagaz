import json

from django.http import HttpResponseRedirect
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from goods.models import Category

from goods.serializers import CategorySerializers
from payment.serializers import CreatePaymentSerializer
from payment.services.create_payment import create_payment_yookassa
from payment.services.payment_acceptance import payment_acceptance
from salemagaz.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


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
class CategoryAPIListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 10000


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    pagination_class = CategoryAPIListPagination


class CategoryAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (IsAuthenticated,)

    # доступ только по токенам, по сессиям и др. не получится.
    # authentication_classes = (TokenAuthentication,)


class CategoryAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = (IsAdminOrReadOnly,)


class CreatePaymentAPIView(generics.CreateAPIView):
    serializer_class = CreatePaymentSerializer
    return_url = "http://127.0.0.1:8000/api/crate_payment/"

    def post(self, request, *args, **kwargs):
        serializer = CreatePaymentSerializer(data=request.POST)
        if serializer.is_valid():
            payment = create_payment_yookassa(serializer.validated_data)

            return HttpResponseRedirect(payment.confirmation.confirmation_url)
        return Response(status=400)


class CreatePaymentAcceptanceView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        response = json.loads(request.body)
        print(response)
        if payment_acceptance(response):
            print("CreatePaymentAcceptanceView")
            return Response(200)
        return Response(404)


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
