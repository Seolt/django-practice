# from django import forms
# from .models import CustomUser
# from django.contrib.auth.forms import UserCreationForm

# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'user_type', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'location', 'about', 'phone', 'email', 'user_image']
        
        widgets = {
            'user_image': forms.FileInput(attrs={'style': 'display: none;', 'id': 'id_user_image'}),
        }
class UserPermissionsForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        choices=[('user', 'User'), ('admin', 'Admin'), ('facilitator', 'Facilitator')],
        widget=forms.Select(attrs={'class': 'selectize-dropdown-content'}),
        required=True
    )
    can_login = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['user_type', 'can_login']
class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'remember_me')