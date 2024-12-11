from django.contrib import admin
from .models import *

class WorkAdmin(admin.ModelAdmin):
    list_display = ('id','name','duration','price','note','id_employee')

class RequestJobAdmin(admin.ModelAdmin):
    list_display = ('id','id_work','id_client','date_start','date_finish','note','result')

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id','mark','country','date_release')

admin.site.register(Work,WorkAdmin)
admin.site.register(RequestJob,RequestJobAdmin)
admin.site.register(Equipment,EquipmentAdmin)

