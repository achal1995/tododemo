from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import List,Avatar
User = get_user_model()


def index(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            task = request.POST.get('task')
            dellall=request.POST.get('deleteall')
            #will add task to the session variable
            if task:
                todo_tasks = request.session.get('todo_tasks', [0])
                if not request.user.is_authenticated:
                    if len(todo_tasks)<=5:
                        todo_tasks.append(task)
                    else:
                        messages.error(request,'Max 5 items allowed for unregisterd user.')
                else:
                    todo_tasks.append(task)
                request.session['todo_tasks']=todo_tasks

                context = {
                    'todo_tasks':todo_tasks,
                }
                return render(request,'pages/index.html',context)
            elif dellall:
                if dellall == "del_all":
                    del request.session['todo_tasks']
                todo_tasks = request.session.get('todo_tasks', [0])
                request.session['todo_tasks']=todo_tasks

                context = {
                    'todo_tasks':todo_tasks,
                }
                return render(request,'pages/index.html',context)
            else:
                dellitem=request.POST.get('deleteitem')
                request.session['todo_tasks'].remove(dellitem)
                todo_tasks = request.session.get('todo_tasks', [0])
                request.session['todo_tasks']=todo_tasks

                context = {
                    'todo_tasks':todo_tasks,
                }
                return render(request,'pages/index.html',context)
        else:
            task = request.POST.get('task')
            dellall=request.POST.get('deleteall')
            if task:
                item=List(content=task,owner=request.user)
                item.save()
                return redirect(index)
            elif dellall:
                if dellall == "del_all":
                    List.objects.filter(owner=request.user).delete()      
                return redirect(index)
            else:
                dellitem=request.POST.get('deleteitem')
                List.objects.filter(content__exact=dellitem,owner=request.user).delete()
                return redirect(index)


    else:
        if not request.user.is_authenticated:
            todo_tasks = request.session.get('todo_tasks', [0])
            request.session['todo_tasks']=todo_tasks

            context = {
                'todo_tasks':todo_tasks,
            }
            return render(request,'pages/index.html',context)
        else:
            todo_tasks = List.objects.filter(owner__exact=request.user)
            context = {
                'todo_tasks':todo_tasks,
            }
            return render(request,'pages/index.html',context)


def about(request):
    return render(request,'pages/about.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user=auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('index')
            else:
                messages.error(request,'Invalid Credentials.')
                return redirect('login')
        else:
            return render(request,'registration/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            password1 = request.POST.get('pass1')
            password2 = request.POST.get('pass2')
            #check if password match
            if password1 == password2:
                #check email
                User=get_user_model()
                if (User.objects.filter(email=email).exists()):
                    messages.error(request,'Email already exists.')
                    return redirect('register')
                else:
                    user=User.objects.create_user(email=email, password=password2,full_name=fullname)
                    user.save()
                    messages.success(request, 'You are now registered and can login.')
                    return redirect('login')
            else:
                messages.error(request,'Passwords do not match.')
                return redirect('register')
        else:
            return render(request,'registration/register.html')

@login_required
def dashboard(request):
    profilepic=Avatar.objects.filter(owner__exact=request.user)
    if profilepic.exists():
        context={
            'profilepic':profilepic[0],
        }
    else:
        context={
            'profilepic':'avatars/default.jpg'
        }
    return render(request,'pages/dashboard.html',context)
@login_required
def edit(request):
    if request.method =="POST":
        pic=request.FILES.get('avatar')
        name=request.POST.get('name')
        if pic:
            Avatar.objects.update_or_create(owner=request.user,defaults={"avatar":pic})
        if name:
            User.objects.update_or_create(email=request.user.email,defaults={"full_name":name})
        messages.success(request, 'Profile Updated!')
    return render(request,'pages/edit.html')