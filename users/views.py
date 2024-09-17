from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from orders.models import Order, OrderItem

from carts.models import Cart
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    # success_url = reverse_lazy("main:index")

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                # if forgot_carts.exists():
                #     forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f"{user.username}, вы вошли в аккаунт")
                return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "SaleMagaz - Авторизация"
        return context


class UserRegistrationView(CreateView):
    template_name = "users/login.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        messages.success(self.request, f"{user.username}, вы вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = self.get_context_data(**kwargs)
        context["title"] = "SaleMagaz - Регистрация"
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("user:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлен.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "SaleMagaz - Личный кабинет"
        # У меня заказы отдельно в orders/views
        # context["orders"] = (
        #     Order.objects.filter(user=self.request.user)
        #     .prefetch_related(
        #         Prefetch(
        #             "orderitem_set",
        #             queryset=OrderItem.objects.select_related("product"),
        #         )
        #     )
        #     .order_by("-id")
        # )
        return context


class UserCartView(TemplateView):
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex["title"] = "SaleMagaz - Корзина"
        return contex


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, вы вышли из акканута")
    auth.logout(request)
    return redirect(reverse("main:index"))


# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             # username = request.POST["username"]
#             # password = request.POST["password"]
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(username=username, password=password)
#
#             session_key = request.session.session_key
#
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, вы вошли в акканут")
#
#                 if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)
#
#                 redirect_page = request.POST.get("next", None)
#                 if redirect_page and redirect_page != reverse("user:logout"):
#                     return HttpResponseRedirect(request.POST.get("next"))
#                 return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserLoginForm()
#
#     context = {
#         "title": "SaleMagaz - Авторизация",
#         "form": form,
#     }
#     return render(request, "users/login.html", context)


# def registration(request):
#
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#
#             session_key = request.session.session_key
#
#             user = form.instance
#             auth.login(request, user=user)
#
#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)
#
#             messages.success(request, f"{user.username}, вы успешно зарегестрировались")
#             return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserRegistrationForm()
#
#     context = {
#         "title": "SaleMagaz - Регистрация",
#         "form": form,
#     }
#     return render(request, "users/login.html", context)
#


# @login_required
# def profile(request):
#
#     if request.method == "POST":
#         form = ProfileForm(
#             data=request.POST, instance=request.user, files=request.FILES
#         )
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Профиль обновлен")
#             return HttpResponseRedirect(reverse("user:profile"))
#     else:
#         form = UserRegistrationForm(instance=request.user)
#
#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 "orderitem_set",
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         )
#         .order_by("-id")
#     )
#     context = {
#         "title": "SaleMagaz - Личный кабинет",
#         "form": form,
#     }
#     return render(request, "users/profile.html", context)

#
# def users_cart(request):
#     return render(request, "users/users_cart.html")
