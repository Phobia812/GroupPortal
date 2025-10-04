import os
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.views.generic import FormView
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser

def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = request.build_absolute_uri(
        reverse('activate', kwargs={'uidb64': uid, 'token': token})
    )

    subject = "Активація акаунта"
    message = render_to_string("accounts/activation_email.html", {
        'user': user,
        'activation_link': activation_link,
    })

    send_mail(
        subject,
        message,
        os.getenv("EMAIL_LOGIN"),
        [user.email],
        fail_silently=False,
    )

class ActivateView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            messages.success(request, "Акаунт успішно активовано! Тепер можете увійти.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Посилання недійсне або прострочене.")
            return redirect('accounts:login')

class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "profile_form" not in context:
            context["profile_form"] = UserProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            user.first_name = profile.first_name
            user.last_name = profile.last_name
            user.save()

            send_verification_email(request, user)
            messages.success(request, "Перевірте ваш email для активації акаунта!")
            return redirect("accounts:login")

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{form.fields[field].label if field in form.fields else field}: {error}")
        for field, errors in profile_form.errors.items():
            for error in errors:
                messages.error(request, f"{profile_form.fields[field].label if field in profile_form.fields else field}: {error}")

        return render(request, self.template_name, {"form": form, "profile_form": profile_form})

class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            if not user.email_verified:
                messages.error(request, "Ваш акаунт не активовано. Перевірте ваш email.")
            elif not user.is_active:
                messages.error(request, "Ваш акаунт заблокований")
            else:
                login(request, user)
                messages.success(request, f"Ласкаво просимо, {user.username}!")
                return redirect("home:home")
        else:
            messages.error(request, "Невірний логін або пароль")

        return render(request, self.template_name)

@login_required
def logout_view(request):
    username = request.user.username
    list(messages.get_messages(request))
    logout(request)
    messages.success(request, f"До побачення, {username}!")
    return redirect('accounts:login')

class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request):
        profile_form = UserProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {"profile_form": profile_form})

    def post(self, request):
        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if profile_form.is_valid():
            profile = profile_form.save()

            request.user.first_name = profile.first_name
            request.user.last_name = profile.last_name
            request.user.save()

            messages.success(request, "Профіль успішно оновлено!")
            return redirect("accounts:profile")
        else:
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"{profile_form.fields[field].label if field in profile_form.fields else field}: {error}")

        return render(request, self.template_name, {"profile_form": profile_form})