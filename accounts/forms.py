from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Ім'я користувача"
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Підтвердіть пароль"
        
        self.fields['email'].required = True

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата народження"
    )

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'birth_date', 'avatar', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "Ім'я"
        self.fields['last_name'].label = "Прізвище"
        self.fields['birth_date'].label = "Дата народження"
        self.fields['avatar'].label = "Аватар"
        self.fields['bio'].label = "Про себе"

class AdminUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')