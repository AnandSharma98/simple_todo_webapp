import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # this is used to specify that login is required to access


# particular page


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == "GET":  # agar get h toh form dikao
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:  # else create new user
        if request.POST['password1'] == request.POST[
            'password2']:  # ye names jo h textfield ke h passwords wale jo form me h , so inspect ki help se dek skta h
            try:
                # here creating user and saving it
                user = User.objects.create_user(request.POST['username'])
                user.set_password(request.POST['password1'])
                user.save()
                login(request, user)  # to keep logged in the user
                return redirect('currenttodos')

            except IntegrityError:  # this error is thrown basically when you try to use existing user for signup
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'that username '
                                                                                                     'already taken'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Password did not '
                                                                                                 'match'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)  # yeh islie kuki hume user specific
    # todoo dikana h , vo b jo complete nhi hua h that's y datecompleted__isnull=True is used
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


# yaha login.html se loginuser kia h
def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # just checking if user exits or not
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)  # to keep logged in the user
            return redirect('currenttodos')


@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)  # melting info back to form just to keep hold
            new_to_do = form.save(commit=False)  # it will not actually save the data in db
            new_to_do.user = request.user  # added user (vhi foreign key)
            new_to_do.save()  # now putting that data back to database
            return redirect('currenttodos')  # redirected to current
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in'})
            # this error is when user typed too long title


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)  # user wala part islie such that , hum url me mje
    # lekr dusre ki todoo na dek pae
    if request.method == "GET":  # when req is get , show the form with data
        form = TodoForm(instance=todo)  # this is to grab that todoo info and to show the form of todoo filled with
        # this info , its basically filling out the form automatically with that form kind of instance
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:  # else  do post thing if demanded to save
        try:
            # these are to get the save request and save that info of form and be redirected to current page again
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'form': todo, 'error': 'Bad info'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()  # ye set krne se , ab vo null nhi raha , so show up ni hoga
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodos')


@login_required
def completedtodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    # yeh islie kuki hume user specific todoo dikana h , vo b jo complete hua h that's y datecompleted__isnull= False is
    # used, orderby - to show recent ones
    return render(request, 'todo/completedtodos.html', {'todos': todos})
