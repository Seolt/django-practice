from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.templatetags.static import static
from .forms import RegistrationForm, UserProfileForm, UserPermissionsForm, CustomAuthenticationForm
from .models import CustomUser

def index(request):
    return render(request, 'Wendy/index.html')
def dynamic_url(request, url):
    if url == 'favicon.ico':
        return HttpResponseRedirect(static('favicon.ico'))
    url+='.html'
    return render(request, 'Wendy/'+ url)
def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.can_login:
                    auth_login(request, user)
                    if remember_me:
                        request.session['remember_me'] = 'true'
                        request.session.set_expiry(1209600)  # 2 weeks
                    else:
                        request.session['remember_me'] = 'false'
                        request.session.set_expiry(0)  # Browser session
                    return redirect('Wendy:index')
                else:
                    messages.error(request, "You do not have permission to log in.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
        if 'remembered_username' in request.COOKIES:
            form.fields['username'].initial = request.COOKIES['remembered_username']
        if 'remember_me' in request.COOKIES:
            form.fields['remember_me'].initial = request.COOKIES['remember_me'] == 'true'
    return render(request, 'Wendy/sign-in.html', {'form': form})
def register(request):
    if request.method == 'POST':
        # Create a form that has request.POST
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the user's password securely
            username = form.cleaned_data['username']         
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:
                user.set_password(password1)
                user.save()
                print(user)
                
                send_Email(request)
                return redirect('Wendy:login')  # Redirect to the login page
            else:
                # Handle password mismatch error here
                form.add_error('password2', 'Passwords entered do not match')
                messages.error(request, 'Please re-enter your password')
        else:
            messages.error(request, 'Enter the password within 8 to 24 characters by combining at least two types of English letters and numbers and special characters.')
    else:
        form = RegistrationForm()
    return render(request, 'Wendy/register.html', {'form': form})
def logout(request):
    response = redirect('Wendy:login')
    if request.session.get('remember_me', 'false') == 'true':
        response.set_cookie('remembered_username', request.user.username, max_age=3600*24*30)  # Cookie lasts for 30 days
        response.set_cookie('remember_me', 'true', max_age=3600*24*30)
    else:
        response.delete_cookie('remembered_username')
        response.delete_cookie('remember_me')
    auth.logout(request)
    return response

    
def send_Email(request):
    subject="Welcome!"
    to=[request.POST.get('email')]
    from_email=settings.DEFAULT_FROM_EMAIL
    message="가입을 환영합니다"
    send_mail(subject, message, from_email, to, fail_silently=False)
    
@login_required
def changepassword(request):
    if request.method=='POST':
        user=request.user
        current_password=request.POST.get('current_password')
        new_current_password=request.POST.get('new_current_password')
        repeat_new_current_password=request.POST.get('repeat_new_current_password')
        if new_current_password==repeat_new_current_password:
            user.set_password(new_current_password)
            user.save()
            return render(request, 'Wendy/complete-change-password.html')
    else:
        return render(request, 'Wendy/change-password.html')
    
@login_required
def upload_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Wendy:index')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "Wendy/my-profile.html", {'form': form})
@login_required
def bookmark(request):
    return render(request, "Wendy/bookmarks.html")
@login_required
def my_ads(request):
    return render(request, "Wendy/my-ads.html")
@login_required
def sold_items(request):
    return render(request, "Wendy/sold-items.html")

@user_passes_test(lambda u: u.is_superuser)
def manage_permissions(request):
    if request.method == 'POST':
        form = UserPermissionsForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(id=request.POST.get('user_id'))
            can_login = form.cleaned_data.get('can_login')
            user_type = form.cleaned_data.get('user_type')

            user.can_login = can_login
            user.user_type = user_type
            user.save()
            return redirect('Wendy:manage_permissions')
    else:
        users = CustomUser.objects.all()
        forms = {user.id: UserPermissionsForm(instance=user) for user in users}

    return render(request, 'Wendy/manage-permissions.html', {'forms': forms})