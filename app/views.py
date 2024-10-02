from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import LoginForm, SignupForm
from django.contrib.auth.forms import PasswordChangeForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Foydalanuvchi nomi yoki parol noto‘g‘ri.')
        else:
            messages.error(request, 'Foydalanuvchi nomi yoki parol noto‘g‘ri.')
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.error(request, "Siz saytdan chiqib ketdingiz!!! \n"
                        "Kirish uchun login parolingizni kiriting!!")
        return redirect('login')

User = get_user_model()

class RegisterView(FormView):
    form_class = SignupForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Bu yerda `form.save()` dan foydalangandan ko'ra, `User` obyekti yaratamiz
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login')
        return render(request, 'register.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')

class UserProfileView(View):
    def get(self, request):
        context = {
            'title': 'Profile',
            'image': 'https://media.istockphoto.com/id/1300845620/vector/user-icon-flat-isolated-on-white-background-user-symbol-vector-illustration.jpg?s=612x612&w=0&k=20&c=yBeyba0hUkh14_jgv1OKqIH0CCSWU_4ckRkAoy2p73o='
        }
        return render(request, 'profile.html', context)

    def post(self, request: WSGIRequest):
        if request.user.is_authenticated:
            user = request.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            if 'phone_number' in request.POST:
                user.phone_number = request.POST['phone_number']
            user.save()

            return redirect('profile')



class UpdateProfileImageView(LoginRequiredMixin, View):
    def post(self, request):
        if 'image' in request.FILES:
            photo = request.FILES['image']
            if photo.name.endswith(('.jpg', '.jpeg', '.png')):
                user = request.user
                user.photo = photo
                user.save()
                messages.success(request, 'Profil rasmi o\'zgartirildi!')
            else:
                messages.error(request, 'Noto\'g\'ri fayl formati. JPG, JPEG yoki PNG formatidagi rasmni tanlang.')
                return redirect('profile')
        messages.error(request, 'Rasmni yuklashda xato!')
        return redirect('profile')

class CustomChangePasswordView(View):
    # def post(self,request):
    #     form = PasswordChangeForm(request.user, data=request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user)
    #         messages.success(request, 'Parolingiz qaydi shakllandi')
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'Parolni to' 'gri qilgan va yoki tugmasini bos qilingan')
    #         return redirect('password_change')

    def post(self, request):
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return redirect('login')
        return redirect('profile')
