from django.shortcuts import render
from basic_app.forms import Userform,UserPortfolioForm
#for login
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

#if we wannt to something special to user for this login required
@login_required
def special(request):
    return HttpResponse('you are loggedin nice!!')

#inbuilt decorators for logout login required
@login_required
def user_logout(request):
    #django inbuilt method
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = Userform(data = request.POST)
        profile_form = UserPortfolioForm(data = request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user = user#ONE TO ONE RELATION

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = Userform()
        profile_form = UserPortfolioForm()

    return render(request,'basic_app/registration.html',{'user_form':user_form
    ,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        #django in-built method to check username and password in database
        user=authenticate(username=username,password=password)
        # if user avilable
        if user:
            if user.is_active:
                #django inbuilt function
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('someone tried to login and failed')
            print('username: {} and password {}'.format(username,password))
            return HttpResponse('invalid login details supplied!!')
    else:
        return render(request,'basic_app/login.html',{})
