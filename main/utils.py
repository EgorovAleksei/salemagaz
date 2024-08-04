import json

from django.db.models import Q

from goods.models import Category

MENU = {}
CATEGORIES = {}


def get_menu_cat():
    global MENU, CATEGORIES
    categories = (Category.objects.filter(level=0))
    for cat in categories:
        CATEGORIES[cat.id] = {'name': cat.name}
        CATEGORIES[cat.id]['url'] = cat.url
        if cat.childs:
            cat_level_1 = Category.objects.filter(Q(level=1) & Q(parent=cat.id))
            CATEGORIES[cat.id]['children'] = {}
            child1 = CATEGORIES[cat.id]['children']
            for cat_level1 in cat_level_1:
                child1[cat_level1.id] = {'name': cat_level1.name}
                child1[cat_level1.id]['url'] = cat_level1.url

                if cat_level1.childs:
                    cat_level_2 = Category.objects.filter(Q(level=2) & Q(parent=cat_level1.id))
                    child1[cat_level1.id]['children'] = {}
                    child2 = child1[cat_level1.id]['children']
                    for cat_level2 in cat_level_2:
                        child2[cat_level2.id] = {'name': cat_level2.name}
                        child2[cat_level2.id]['url'] = cat_level2.url

    return CATEGORIES
