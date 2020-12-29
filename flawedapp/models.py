from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ToDoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=200)

class CreditCards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    cardnumber = models.CharField(max_length=20)
    csc = models.CharField(max_length=4)

