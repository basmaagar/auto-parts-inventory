from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserFrom, ProfileUpdateForm , UserUpdateForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'user/login.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('index')  # dashboard
        else:
            return reverse_lazy('product')  # catalog

def register(request):
    print("Register view called with method:", request.method)
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('user_login')
        else:
            messages.error(request, 'Please correct the errors below.')
            print("Form errors:", form.errors)
            return render(request, 'user/register.html', {'form': form, 'errors': form.errors})
    else:
        form = CreateUserFrom()
    return render(request, 'user/register.html', {'form': form})


def logout_page(request):
    return render(request, 'user/logout.html')


@login_required


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/profile_update.html', context)


def profile(request):
    return render(request, 'user/profile.html') 

