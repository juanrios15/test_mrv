from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy


class LoginMrvView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    fields = ['email', 'password']

    def get_success_url(self):
        return reverse_lazy("home")


class LogoutMrvView(LogoutView):
    next_page = reverse_lazy("home")


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


class RegisterMrvView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('users_app:login')

    def post(self, request, *args, **kwargs): # Imprime los datos POST para depurar
        self.form_class(request.POST)  # Imprime si el formulario es válido
        return super().post(request, *args, **kwargs)
