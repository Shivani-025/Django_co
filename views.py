from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
# Create your views here.
#def home(request):
  #return render(request, 'receipe.html')
@login_required(login_url="/login_page/")
def receipe(request):
  
    if request.method == "POST":
        
        data = request.POST
        
        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_des = data.get('receipe_des')
        
        
        print(receipe_name)
        print(receipe_des)
        
        Receipe.objects.create(
          receipe_name = receipe_name,
          receipe_des = receipe_des,
          receipe_img = receipe_img,  
        )
        
        return redirect('/receipe')
    query = Receipe.objects.all()
    
    if request.GET.get('search'):
      print(request.GET.get('search'))
      query = query.filter(receipe_name__icontains = request.GET.get('search'))               # __icontains use for  'given character/string name' like 'P' so it filter all P recienpe_name
      
    context = {'receipe' : query}
    return render(request, 'receipe.html', context )
  
def update_receipe(request, id):
  query = Receipe.objects.get(id = id)
  if request.method == "POST":
        
        data = request.POST
        
        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_des = data.get('receipe_des')
        
        query.receipe_name = receipe_name
        query.receipe_des = receipe_des
        
        if receipe_img:
          query.receipe_img = receipe_img
        query.save()
        return redirect('/receipe')
  context = {'receipe' : query}
  return render(request, 'update_receipe.html', context)

def delete_receipe(request, id):
    print(id)
    try:
        receipe = Receipe.objects.get(id=id)
        print(receipe.delete())
        return redirect('/receipe')
    except Receipe.DoesNotExist:
        return HttpResponse("Receipe not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
      
def login_page(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
     
    if not User.objects.filter(username = username).exists():
      messages.error(request, 'Invalid Username')
      return redirect('/login_page/')
      
    user = authenticate(username = username , password = password)
      
    if user is None:
      messages.error(request, 'Invalid Password')
      return redirect('/login_page/')
    else:
      login(request, user)
      return redirect('/receipe')
    
  return render(request, 'login.html' )      

def logout_page(request):
    logout(request)
    return redirect('/login_page/')

def register(request):
  if request.method == "POST":
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = User.objects.filter(username = username)
    
    if user.exists():
      messages.info(request, 'Username already taken')
      return redirect('/register/')
    
    user = User.objects.create(
      first_name = first_name,
      last_name = last_name,
      username = username,
    )
    user.set_password(password)
    user.save()
    
     
    
    messages.info(request, 'Account created Successfully')

    return redirect('/register/')
    
  return render(request, 'register.html')
        
        
        