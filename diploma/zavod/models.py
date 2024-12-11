from django.db import models
from django.contrib.auth.models import User


class Work(models.Model):
    name = models.CharField(max_length=255)
    duration = models.IntegerField(blank=False)
    price = models.IntegerField(default=0)
    difficult = models.CharField(max_length=255)
    note = models.TextField(max_length=255)
    garantiya = models.IntegerField(default=1)
    id_employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True)


    def __str__(self):
        return self.name

class Equipment(models.Model):
    mark = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    srok_sl = models.IntegerField(max_length=255)
    garantiya = models.IntegerField(max_length=255)
    price = models.IntegerField(max_length=255)
    country = models.CharField(max_length=255)
    date_release = models.DateField()
    def __str__(self):
        return self.mark


class RequestJob(models.Model):
    id_work = models.ForeignKey(Work, on_delete=models.PROTECT, null=True)
    id_client = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, null=True)
    #id_employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    note = models.TextField()
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField()
    result = models.BooleanField(default=False)
    def __str__(self):
        return self.id_work


