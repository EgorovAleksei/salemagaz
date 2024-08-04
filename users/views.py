from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib import auth, messages
from django.urls import reverse

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


# Create your views here.


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # username = request.POST["username"]
            # password = request.POST["password"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, вы вошли в акканут")
                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse("user:logout"):
                    return HttpResponseRedirect(request.POST.get("next"))
                return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserLoginForm()

    context = {
        "title": "SaleMagaz - Авторизация",
        "form": form,
    }
    return render(request, "users/login.html", context)


def registration(request):

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user=user)
            messages.success(request, f"{user.username}, вы успешно зарегестрировались")
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "SaleMagaz - Регистрация",
        "form": form,
    }
    return render(request, "users/login.html", context)


@login_required
def profile(request):

    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request, f"Профиль обновлен")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = UserRegistrationForm(instance=request.user)

    context = {
        "title": "SaleMagaz - Личный кабинет",
        "form": form,
    }
    return render(request, "users/profile.html", context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, вы вышли из акканута")
    auth.logout(request)
    return redirect(reverse("main:index"))


def users_cart(request):
    print(request.path)
    return render(request, "users/users_cart.html")
