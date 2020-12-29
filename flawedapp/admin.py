from django.contrib import admin

# Register your models here.

from .models import ToDoItem, CreditCards

admin.site.register(ToDoItem)
admin.site.register(CreditCards)