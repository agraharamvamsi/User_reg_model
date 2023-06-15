from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required



# Create your views here.


def home(request):
    if request.session.get('username'):
        username = request.session.get('username')
        d = {'username' : username}
        return render(request, 'home.html', d)
    return render(request, 'home.html')

def registration(request):
    ufo = userform()
    pfo = profileform()
    d = {'ufo' : ufo, 'pfo' : pfo}
    if request.method == 'POST' and request.FILES:
        ufd = userform(request.POST)
        pfd = profileform(request.POST, request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            nsuo = ufd.save(commit = False)
            nsuo.set_password(ufd.cleaned_data['password'])
            nsuo.save()

            nspo = pfd.save(commit = False)
            nspo.username = nsuo
            nspo.save()

            return HttpResponse('Regsitration is Susssessfulll')

        else:
            return HttpResponse('invalid data')
    return render(request, 'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        AUO = authenticate(username = username, password = password)
        if AUO and AUO.is_active:
            login(request, AUO)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalied data')
    return render(request, 'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_profile(request):
    username = request.session.get('username')
    uo = User.objects.get(username = username)
    po = Profile.objects.get(username = uo)
    d = {'uo' : uo, 'po' : po}

    return render(request, 'display_profile.html', d)



@login_required
def change_password(request):
    if request.method == 'POST':
        pw = request.POST['pw']
        username = request.session.get('username')
        uo = User.objects.get(username = username)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('<h1> Password changed successfully </h1>')
    return render(request, 'change_password.html')


def forget_password(request):
    if request.method == 'POST':
        un = request.POST['un']
        pw = request.POST['pw']
        uno = User.objects.filter(username = un)   
        if uno:
            uno[0].set_password(pw)
            uno[0].save()
            return HttpResponse('<center><h1>Password reset done</h1></center>')

        else:
            return HttpResponse('<center><h1>User not available</h1></center>')
    return render(request, 'forget_password.html')