from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from zavod.models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import *
from zavod.forms import *
from .utils import *
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
from django.contrib import messages
from django.contrib.auth.models import Group


class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))
    def form_valid(self, form):
        user = form.save()
        g = Group.objects.get(name='clients')
        user.groups.add(g)
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin,LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

class EquipmentList(LoginRequiredMixin,DataMixin,ListView):
    login_url = 'login/'
    redirect_field_name = ''
    model = Equipment
    template_name = 'equipments.html'
    context_object_name = 'posts'
    #extra_context = {'title': 'Главная страница'}
    success_url = reverse_lazy('home')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список оборудования")
        return dict(list(context.items()) + list(c_def.items()))

class ShowEquipment(LoginRequiredMixin,DataMixin,DetailView):
    login_url = 'login/'
    redirect_field_name = ''
    model = Equipment
    context_object_name = 'post'
    template_name = 'equipment.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оборудование')
        return dict(list(context.items()) + list(c_def.items()))

class RequestJobList(LoginRequiredMixin,DataMixin,ListView):
    login_url = 'login/'
    redirect_field_name = ''
    model = RequestJob
    template_name = 'requestsJob.html'
    context_object_name = 'posts'
    #extra_context = {'title': 'Главная страница'}
    success_url = reverse_lazy('home')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Заявки")
        return dict(list(context.items()) + list(c_def.items()))
    def get_queryset(self):
        if self.request.user.username !='root':
            if str(self.request.user.groups.all()[0]) == 'clients':
                return RequestJob.objects.filter(id_client_id=self.request.user.id)
            if str(self.request.user.groups.all()[0]) == 'employee':
                work = Work.objects.filter(id_employee_id = self.request.user.id)
                work_list = list()
                print(work)
                for w in work:
                    work_list.append(RequestJob.objects.filter(id_work_id=w.id))

                for wor in work_list:
                    all = work_list[0].union(wor)

                return all
        return RequestJob.objects.all()

class ShowRequestJob(LoginRequiredMixin,DataMixin,DetailView):
    login_url = 'login/'
    redirect_field_name = ''
    model = RequestJob
    context_object_name = 'post'
    template_name = 'requestJob.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Заявка')
        return dict(list(context.items()) + list(c_def.items()))


class WorkList(LoginRequiredMixin,DataMixin,ListView):
    login_url = 'login/'
    redirect_field_name = ''
    model = Work
    template_name = 'works.html'
    context_object_name = 'posts'
    #extra_context = {'title': 'Главная страница'}
    success_url = reverse_lazy('home')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Список услуг")
        return dict(list(context.items()) + list(c_def.items()))

class ShowWork(LoginRequiredMixin,DataMixin,DetailView):
    login_url = 'login/'
    redirect_field_name = ''
    model = Work
    context_object_name = 'post'
    template_name = 'work.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Услуга')
        return dict(list(context.items()) + list(c_def.items()))

#@permission_required('zavod.change_requestjob')
class EmployeeList(PermissionRequiredMixin,LoginRequiredMixin,DataMixin,ListView):
    permission_required = 'zavod.change_requestjob'
    login_url = 'login/'
    redirect_field_name = ''
    model = User
    template_name = 'users.html'
    context_object_name = 'posts'
    #extra_context = {'title': 'Главная страница'}
    success_url = reverse_lazy('home')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Сотрудники")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return User.objects.filter(groups__name='employee')

class ShowEmployee(PermissionRequiredMixin,LoginRequiredMixin,DataMixin,DetailView):
    permission_required = 'zavod.change_requestjob'
    login_url = 'login/'
    redirect_field_name = ''
    model = User
    context_object_name = 'post'
    template_name = 'user.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Сотрудник')
        return dict(list(context.items()) + list(c_def.items()))

class AddRequestJob(LoginRequiredMixin,DataMixin,CreateView):
    login_url = 'login/'
    redirect_field_name = ''
    form_class = AddPostForm
    template_name = 'addrequestjob.html'
    success_url = reverse_lazy('requestsJob')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление заявки")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        dat = form.cleaned_data
        work = dat['id_work']
        RequestJob.objects.create(id_work=dat['id_work'],id_client_id=self.request.user.id,equipment=dat['equipment'],
                                  date_finish=datetime.datetime.now()+ datetime.timedelta(days=work.duration),note=dat['note'])
        return redirect('requestsJob')


class RequestJobUpdate(PermissionRequiredMixin,LoginRequiredMixin,DataMixin,UpdateView):
    permission_required = 'zavod.change_requestjob'
    raise_exception = True
    login_url = 'login/'
    redirect_field_name = ''
    model = RequestJob
    fields = ['id_work','equipment', 'note', 'date_finish','result']
    success_url = reverse_lazy('requestsJob')
    template_name = 'updaterequestjob.html'
    def form_valid(self, form):
        messages.success(self.request, "The task was updated successfully.")
        return super(RequestJobUpdate, self).form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редактирование заявки')
        return dict(list(context.items()) + list(c_def.items()))

class RequestJobDelete(LoginRequiredMixin,DataMixin,DeleteView):
    login_url = 'login/'
    context_object_name = 'pos'
    redirect_field_name = ''
    model = RequestJob
    success_url = reverse_lazy('requestsJob')
    template_name = 'deleterequestjob.html'

    def form_valid(self, form):
        messages.success(self.request, "The task was delete successfully.")
        return super(RequestJobDelete, self).form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удаление заявки')
        return dict(list(context.items()) + list(c_def.items()))

class AddWork(PermissionRequiredMixin,LoginRequiredMixin,DataMixin,CreateView):
    permission_required = 'zavod.change_requestjob'
    login_url = 'login/'
    redirect_field_name = ''
    form_class = AddWork
    template_name = 'addwork.html'
    success_url = reverse_lazy('works')
    raise_exception = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление работы")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        return super(AddWork, self).form_valid(form)

class WorkUpdate(PermissionRequiredMixin,LoginRequiredMixin,DataMixin,UpdateView):
    permission_required = 'zavod.change_work'
    raise_exception = True
    login_url = 'login/'
    redirect_field_name = ''
    model = Work
    fields = ['name','duration','price', 'note','id_employee']
    success_url = reverse_lazy('works')
    template_name = 'updatework.html'
    def form_valid(self, form):
        messages.success(self.request, "The work was updated successfully.")
        return super(WorkUpdate, self).form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редактирование работы')
        return dict(list(context.items()) + list(c_def.items()))

class WorkDelete(LoginRequiredMixin,DataMixin,DeleteView):
    login_url = 'login/'
    context_object_name = 'pos'
    redirect_field_name = ''
    model = Work
    success_url = reverse_lazy('works')
    template_name = 'deletework.html'

    def form_valid(self, form):
        messages.success(self.request, "The work was delete successfully.")
        return super(WorkDelete, self).form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удаление работы')
        return dict(list(context.items()) + list(c_def.items()))


def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
    # print(self.request.user.groups.all())
    if request.user.groups.all().exists() and str(request.user.groups.all()[0]) == 'clients':
        user_menu.pop(6)
        user_menu.pop(6)
    return render(request, 'about.html',{'menu': user_menu, 'title': 'О сайте'})

def contact(request):
    user = User.objects.all()
    req = RequestJob.objects.all()
  #  print(request.user.id)
   # for r in req:
       # print(r.id_client)
       # print(r.id_client_id)

   # for g in request.user.groups.all():
   #     print(g)
    #print(request.user.groups.all()[0])
    g = Group.objects.get(name='clients')
    #print(g)
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
        user_menu.pop(2)
    # print(self.request.user.groups.all())
    if request.user.groups.all().exists() and str(request.user.groups.all()[0]) == 'clients':
        user_menu.pop(6)
        user_menu.pop(6)
    return render(request, 'contact.html',{'menu': user_menu, 'title': 'Контакты'})


class EquipmentUpdate(PermissionRequiredMixin,LoginRequiredMixin,DataMixin,UpdateView):
    permission_required = 'zavod.change_work'
    raise_exception = True
    login_url = 'login/'
    redirect_field_name = ''
    model = Equipment
    fields = ['mark','country','date_release']
    success_url = reverse_lazy('home')
    template_name = 'updateequipments.html'
    def form_valid(self, form):
        messages.success(self.request, "The equipment was updated successfully.")
        return super(EquipmentUpdate, self).form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редактирование оборудования')
        return dict(list(context.items()) + list(c_def.items()))

class EquipmentDelete(LoginRequiredMixin,DataMixin,DeleteView):
    login_url = 'login/'
    context_object_name = 'posts'
    redirect_field_name = ''
    model = Equipment
    success_url = reverse_lazy('home')
    template_name = 'deleteequipment.html'

    def form_valid(self, form):
        messages.success(self.request, "The equipment was delete successfully.")
        return super(EquipmentDelete, self).form_valid(form)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удаление оборудования')
        return dict(list(context.items()) + list(c_def.items()))
    
class AddEquipment(PermissionRequiredMixin,LoginRequiredMixin,DataMixin,CreateView):
    permission_required = 'zavod.change_requestjob'
    login_url = 'login/'
    redirect_field_name = ''
    form_class = AddEquipment
    template_name = 'addequipment.html'
    success_url = reverse_lazy('home')
    raise_exception = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление оборудования")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        return super(AddEquipment, self).form_valid(form)