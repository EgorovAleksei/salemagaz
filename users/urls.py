from django.urls import path

from users import views

app_name = "users"


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    path("user-cart/", views.UserCartView.as_view(), name="user_cart"),
    path("logout/", views.logout, name="logout"),
    # path("login/", views.login, name="login"),
    # path("registration/", views.registration, name="registration"),
    # path("profile/", views.profile, name="profile"),
    # path("user-cart/", views.users_cart, name="user_cart"),
]
