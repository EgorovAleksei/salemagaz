from django.urls import include, path
from django.views.decorators.cache import cache_page

from main import views

app_name = "main"

urlpatterns = [
    # path("", cache_page(60)(views.IndexView.as_view()), name="index"),
    path("", views.IndexView.as_view(), name="index"),
    # path('about/', views.about, name='about'),
    path("about/", cache_page(60 * 10)(views.AboutView.as_view()), name="about"),
    # path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact, name="contact"),
    # path('__debug__/', include('debug_toolbar.urls')),
]
