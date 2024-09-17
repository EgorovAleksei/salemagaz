from django.urls import include, path

from goods import views
from salemagaz.settings import DEBUG

app_name = "goods"

urlpatterns = [
    path("", views.CatalogView.as_view(), name="index"),
    path("<int:category_id>/", views.CatalogView.as_view(), name="index"),
    path("search/", views.CatalogView.as_view(), name="search"),
    path("product/", views.ProductView.as_view(), name="product"),
    path("product/<int:product_id>/", views.ProductView.as_view(), name="product"),
    # path("", views.catalog, name="index"),
    # path("<int:category_id>/", views.catalog, name="index"),
    # path("search/", views.catalog, name="search"),
    # path('product/', views.product, name='product'),
    # path("product/<int:product_id>/", views.product, name="product"),
]
