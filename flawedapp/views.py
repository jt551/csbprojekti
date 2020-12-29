from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import CreditCards, ToDoItem
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import sqlite3
from django.views.decorators.csrf import csrf_exempt

def index(request):    
    if request.user.is_authenticated:
        todo_list = {}    
        current_user = User.objects.get(username=request.user)
       
        if current_user:
            todo_list = ToDoItem.objects.filter(user=current_user)
           
        return render(request, 'flawedapp/index.html', {'todo_list': todo_list})
    return redirect('/login')

# Flaw 4
@csrf_exempt
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        user = request.user        
        newItem = ToDoItem.objects.create(user=user, title=title, text=text)
        newItem.save()
        return redirect('/flawedapp')
    return HttpResponse("add view")

def delete(request):  
    #Flaw 5
    if request.user.is_authenticated: 
        id = request.GET.get('id')
        print('delete : '+ id)        
        try:
            item = ToDoItem.objects.filter(id=id)
            item.delete()       
        except:
            pass

    return redirect('/flawedapp')

def details(request, id):
    todo_query = ToDoItem.objects.filter(id=id)
    todo_item = { 'todo_item': todo_query }
    return render(request, 'flawedapp/details.html', todo_item)
    

def list(request):
    if request.method == 'GET':        
        data = ToDoItem.objects.filter(user=request.user).values()
        return HttpResponse(data)
    return HttpResponse("unsupported request")
    
def card(request):
    #Flaw 2
    if request.method == 'POST':
        newcard = CreditCards.objects.create(user=request.user, name=request.POST.get('name'), cardnumber=request.POST.get('cardnumber'), csc=request.POST.get('csc'))
        
        newcard.save()
        return redirect('/flawedapp/card/')
    if request.method == 'GET':
        queryresult = CreditCards.objects.filter(user=request.user)
        cards = {'cards': queryresult}
        return render(request, 'flawedapp/card.html', cards)
    return HttpResponse("unsupported request")

def account(request):
    # Flaw 3
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_user = User.objects.get(username=request.user)
            if request.POST.get('password'):
                current_user.set_password(request.POST.get('password'))
                current_user.save()
            return redirect('/flawedapp/account/')
        if request.method == 'GET':
            current_user = User.objects.get(username=request.user)
            userdata = {
                'username': current_user.username,
                'firstname': current_user.first_name,
                'lastname': current_user.last_name,
                'email': current_user.email,                
                }
            print(userdata)
            return render(request, 'flawedapp/account.html', {'userdata': userdata})
        return HttpResponse("unsupported request")
    return redirect('/login')

def search(request):
    #Flaw 1
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        id = int(user.id)
        query_string = request.POST.get('query_string')

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        cursor.execute("SELECT title FROM flawedapp_ToDoItem WHERE id='%s' and text LIKE '%%%s%%'" % (id, query_string)).fetchall()
        results = dictfetchall(cursor)
        
        return render(request, 'flawedapp/search.html', {'results': results})
    return redirect('/login')

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]