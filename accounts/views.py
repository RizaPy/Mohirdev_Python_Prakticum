from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from .forms import LoginForm, UserRegistrationForm, EditProfileForm, userEditForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Registratsiyadan muvaffaqiyatli o\'tdingiz!')
                else:
                    return HttpResponse('Sizning accountingiz faol holatda emas!')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form':form})

def UserProfileView(request):
    user = request.user
    profil = Profile.objects.get(user=user)
    return render(request, 'profile/user-profile.html', {'user':user, 'profil':profil})

def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            Profile.objects.filter(user=new_user).get()


            return render(request, 'signup/register_done.html', context = {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    context = {
            'user_form':user_form
        }
    return render(request, 'signup/register.html', context )

def register_done(request):
    return render(request, 'signup/register_done.html')

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('signup_succes')
    template_name = 'signup/register.html'

# class SignUpSuccessView(TemplateView):
#     template_name = 'signup/register_done.html'
@login_required
def edit_Profile(request):
    # profile_instance = request.user.profile
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, files=request.FILES, instance=request.user.profile)
        profile_form = userEditForm(request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
            #return render(request, 'profile/user_profile.html', {'user_form':user_form, 'profile_form':profile_form})
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = userEditForm(instance=request.user)
    return render(request, 'profile/edit_profile.html', {'user_form':user_form,  'profile_form':profile_form})