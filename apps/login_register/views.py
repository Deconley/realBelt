from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import bcrypt
from .models import User
# Create your views here.
def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def currentUser(request):
    id = request.session['user_id']

    return User.objects.get(id=id)

def index(request):

    return render(request, "login_register/index.html")

def success(request):
    if 'user_id' in request.session:
        current_user = currentUser(request)
        friends = current_user.friends.all()
        users = User.objects.exclude(id__in=friends).exclude(id=current_user.id)

        context = {
        'current_user': current_user,
        'users': users,
        'friends': friends
        }
        # print request.session['user_id']
        return render(request,'login_register/success.html', context)

    return redirect('/')

def register(request):
    if request.method == "POST":
        errors = User.objects.validateRegistration(request.POST)

        if not errors:
            user = User.objects.createUser(request.POST)

            request.session['user_id'] = user.id

            return redirect('/success')
        for error in errors:
            messages.error(request, error)

        flashErrors(request, errors)

    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.validateLogin(request.POST)

        if not errors:
            user = User.objects.filter(email = request.POST['email']).first()
            if user:
                password = str(request.POST['password'])
                user_password = str(user.password)

                hashed_pw = bcrypt.hashpw(password, user_password)

                if hashed_pw == user.password:
                    request.session['user_id'] = user.id

                    return redirect('/success')

            errors.append("Invaid account information")
        flashErrors(request, errors)
    return redirect('/')

def logout(request):
    if 'user_id'in request.session:
        request.session.pop('user_id')
    return redirect('/')

def addFriend(request, id):
    if request.method == "POST":
        if 'user_id' in request.session:
            current_user = currentUser(request)
            friend = User.objects.get(id=id)
            current_user.friends.add(friend)
            return redirect(reverse('success'))
    return redirect(reverse('/'))

def removeFriend(request, id):
        if request.method == "POST":
            if 'user_id' in request.session:
                current_user = currentUser(request)
                friend = User.objects.get(id=id)
                current_user.friends.remove(friend)
                return redirect(reverse('success'))
        return redirect(reverse('/'))

def profile(request, id):
    users = User.objects.filter(id=id)

    context={
        'users' : users
    }

    return render(request, 'login_register/profile.html', context)
