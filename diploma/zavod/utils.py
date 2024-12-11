from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Добавить заявку", 'url_name': 'add_requestjob'},
        {'title': "Виды работ", 'url_name': 'works'},
        {'title': "Оборудование", 'url_name': 'home'},
        {'title': "Заявки", 'url_name': 'requestsJob'},
        {'title': "Сотрудники", 'url_name': 'employees'},
        {'title': "Добавить работу", 'url_name': 'add_work'},
        {'title': "Добавить оборудование", 'url_name': 'add_equipment'},
]

class DataMixin:
    #paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs
        #cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(2)
            user_menu.pop(2)
            user_menu.pop(2)
            user_menu.pop(2)
            user_menu.pop(2)
            user_menu.pop(2)
        #print(self.request.user.groups.all())
        if self.request.user.groups.all().exists() and str(self.request.user.groups.all()[0]) == 'clients':
            user_menu.pop(6)
            user_menu.pop(6)
            user_menu.pop(6)

        context['menu'] = user_menu

        #context['cats'] = cats
        #if 'cat_selected' not in context:
        #    context['cat_selected'] = 0
        return context
