from django.urls import include, path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # path('about/', views.about, name='about'),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact, name="contact"),
    # path('__debug__/', include('debug_toolbar.urls')),
]
