from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .forms import LoginForm, SignUpForm, CustomPasswordResetForm, CustomPasswordChangeForm
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'views/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'views/signup.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            subject = "Password Reset Request"
            content = render_to_string('views/password_reset_email.html', {
                'reset_url': reset_url,
            })
            send_mail(subject, content, 'vinaysingh02640@gmail.com', [email])
            return redirect('login')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'views/forgot_password.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'views/change_password.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'views/dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'views/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')