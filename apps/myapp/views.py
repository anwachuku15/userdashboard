from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'signin.html')

def regpage(request):
    return render(request, 'register.html')

def signin(request):
	result = User.objects.login_validator(request.POST)
	if len(result) > 0:
		for key, value in result.items():
			messages.add_message(request, messages.ERROR, value)
		return redirect('/signin')
	else:
		user = User.objects.get(email = request.POST['email'])
		request.session['userid'] = user.id
		if user.user_level == 9:
			return redirect('/dashboard/admin')
		else:
			return redirect('/dashboard')               
        
def register(request):
    result = User.objects.reg_validator(request.POST)
    allUsers = User.objects.all()
    if len(result) > 0:
        for key, value in result.items():
            messages.add_message(request, messages.ERROR, value)
        print("errors")
        return redirect('/register')
    else:
		# create the user (add to database)
        if len(allUsers) < 1:
            hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(email=request.POST['email'], fname=request.POST['fname'], lname=request.POST['lname'], password=hash.decode(), user_level=9)
        else:
            hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(email=request.POST['email'], fname=request.POST['fname'], lname=request.POST['lname'], password=hash.decode(), user_level=1)
        # save their id in session
        request.session['userid'] = user.id

        if user.user_level == 9:
            return redirect('/dashboard/admin')
        else:
            return redirect('/dashboard')

# when adding messages, disable button if empty

def dashboard(request):
    if 'userid' not in request.session:
        return redirect('/signin')
    else:
        user = User.objects.get(id=request.session['userid'])
        members = User.objects.all()
        context = {
            'user': user,
            'members': members
        }
    return render(request, 'dashboard.html', context)

def admin(request):
    if 'userid' not in request.session:
        return redirect('/signin')
    else:
        user = User.objects.get(id=request.session['userid'])
        members = User.objects.all()
        context = {
            'user': user,
            'members': members
        }
    return render(request, 'admin.html', context)

def addpage(request):
    return render(request, 'addnew.html')

def adduser(request):
    result = User.objects.reg_validator(request.POST)
    allUsers = User.objects.all()
    if len(result) > 0:
        for key, value in result.items():
            messages.add_message(request, messages.ERROR, value)
        print("errors")
        return redirect('/users/new')
    else:
		# create the user (add to database)
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(email=request.POST['email'], fname=request.POST['fname'], lname=request.POST['lname'], password=hash.decode(), user_level=1)

        return redirect('/dashboard/admin')

def editprofile(request):
    user = User.objects.get(id=request.session['userid'])
    myEmail = user.email
    members = User.objects.all()
    context = {
        'user': user,
        'members': members,
        'myemail': myEmail
    }
    print(user.fname)
    return render(request, 'edit.html', context)

def editinfo(request):
    user = User.objects.get(id=request.session['userid'])
    initial = user.email
    result = User.objects.editvalidator(request.POST)
    allUsers = User.objects.all()

    if initial != request.POST['email'] and len(result) > 0:
        for key, value in result.items():
            messages.add_message(request, messages.ERROR, value)
        return redirect('/users/edit')
    else:
        user.email = request.POST['email']
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.save()
        print(user.fname)
    return redirect('/users/edit')

def changepw(request):
    user = User.objects.get(id=request.session['userid'])
    result = User.objects.passwordvalidator(request.POST)

    hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(password=hash.decode())

    return redirect('/users/edit')

def editdesc(request):
    user = User.objects.get(id=request.session['userid'])
    user.description = request.POST['desc']
    print(user.description)
    return redirect('/users/edit')


def profile(request, id):
    user = User.objects.get(id=request.session['userid'])
    msgs = Message.objects.all().order_by("-created_at")
    member = User.objects.get(id=id)
    context = {
        'member': member,
        'user': user,
        'msgs': msgs
    }
    print(reverse('viewprofile', kwargs={'id': id}))
    return render(request, 'profile.html', context)

def postmessage(request, id):
    user = User.objects.get(id=request.session['userid'])
    member = User.objects.get(id=id)
    msg = Message.objects.create(body=request.POST['body'], author=user, profile=member)
    return redirect(reverse('viewprofile', kwargs={'id': id}))

# def postreply(request, id):
#     user = User.objects.get(id=request.session['userid'])
#     msg = User.objects.get(id=id)
    
#     reply = Reply.objects.create(body=request.POST['body'], author=user, message=)


def logout(request):
	request.session.clear()
	return redirect("/signin")