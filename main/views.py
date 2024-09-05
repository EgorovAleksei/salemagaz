from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

from main.templatetags.menu_cat_tags import menu_cat


class IndexView(TemplateView):
    template_name = "main/index.html"
    extra_context = {"title": "SaleMagaz - Главная"}

    # def get(self, request, *args, **kwargs):
    #     categories = menu_cat(request)
    #     return render(request, self.template_name, {'categories': categories})


# def index(request) -> HttpResponse:
#     categories = Category.objects.all()
#     #categories = menu_cat(request)
#     context = {
#         'title': 'SaleMagaz - Главная',
#         #'categories': categories,
#
#     }
#
#     return render(request, template_name='main/index.html', context=context)
#     #return HttpResponse('Home page')


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "SaleMagaz - о магазине"
        context["content"] = "О магазине"
        return context


# def about(request):
#     context = {
#         'title': 'SaleMagaz - о магазине',
#         'content': 'О Магазине'
#     }
#     return render(request, 'main/about.html', context)
#     #return HttpResponse('About')


def contact(request):
    context = {"title": "SaleMagaz - контакты", "content": "Контакты"}
    return render(request, "main/contact.html", context)
