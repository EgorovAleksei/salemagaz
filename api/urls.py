from django.urls import path, include, re_path

from api import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

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
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
