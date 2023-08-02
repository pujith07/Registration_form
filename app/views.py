from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

def home(request):

    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')


def registration(request):
    UFO=UserForm()
    PFO=ProfileForm()
    d={"UFO":UFO,"PFO":PFO}
    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():
            UF=UFD.save(commit=False)
            UF.set_password(UFD.cleaned_data['password'])
            UF.save()
            PF=PFD.save(commit=False)
            PF.username=UF
            PF.save()
            send_mail('registration',(f'thank you for registration {UF.username}'),'pujith2001@gmail.com',[UF.email],fail_silently=False)
            return HttpResponse('registration is successfull')
        else:
            return HttpResponse('invalid data')
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password') 
        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
    
@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=="POST":
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('password changed successfully')
    return render(request,'change_password.html')

def forget_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset successfully')
        else:
            return HttpResponse('username does not exist')
    return render(request,'forget_password.html')