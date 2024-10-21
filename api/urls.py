from django.urls import path, include

from api import views
from rest_framework import routers

app_name = "api"

router = routers.DefaultRouter()

router.register(r"category", views.CategoryViewSet, basename="category")

urlpatterns = [
    # path("v1/", views.ProductListAPIView.as_view()),
    # path("v2/", views.ProductListAPIView.as_view()),
    # path("v2/<int:pk>/", views.ProductAPIUpdate.as_view()),
    path("categorylist/", views.CategoryListAPIView.as_view()),
    path("categorylist/<int:pk>/", views.CategoryAPIUpdate.as_view()),
    path("categorydelete/<int:pk>/", views.CategoryAPIDestroy.as_view()),
    # path("categorydetail/<int:pk>/", views.CategoryAPIUDetailView.as_view()),
    # path("category/", views.CategoryViewSet.as_view({"get": "list"})),
    # path("category/<int:pk>/", views.CategoryViewSet.as_view({"put": "update"})),
    path("v1/", include(router.urls)),
]
