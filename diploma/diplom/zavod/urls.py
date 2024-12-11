from django.urls import path

from .views import *

urlpatterns = [
    #path('', index,name='home'),
    #path('work/<int:workid>/', work,name='work'),
    path('', EquipmentList.as_view(), name='home'),
    path('eq/<int:pk>/', ShowEquipment.as_view(), name='equipment'),
    path('works', WorkList.as_view(), name='works'),
    path('works/<int:pk>/', ShowWork.as_view(), name='work'),
    path('requestsJob', RequestJobList.as_view(), name='requestsJob'),
    path('requestsJob/<int:pk>/', ShowRequestJob.as_view(), name='requestJob'),
    path('employee', EmployeeList.as_view(), name='employees'),
    path('employee/<int:pk>/', ShowEmployee.as_view(), name='employee'),
#    path('employee', EmployeeList.as_view(), name='employee'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('addrequestjob/', AddRequestJob.as_view(), name='add_requestjob'),
    path('requestsJob/update/<int:pk>/', RequestJobUpdate.as_view(), name='requestJob-update'),
    path('requestsJob/delete/<int:pk>/', RequestJobDelete.as_view(), name='requestJob-delete'),
    path('addwork/', AddWork.as_view(), name='add_work'),
    path('works/update/<int:pk>/', WorkUpdate.as_view(), name='work-update'),
    path('works/delete/<int:pk>/', WorkDelete.as_view(), name='work-delete'),
    path('equipment/update/<int:pk>/', EquipmentUpdate.as_view(), name='equipment-update'),
    path('equipment/delete/<int:pk>/', EquipmentDelete.as_view(), name='equipment-delete'),
    path('addequipment/', AddEquipment.as_view(), name='add_equipment')
]