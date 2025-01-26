from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Post


# عرض الصفحة الرئيسية (عرض المنشورات)
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'


# إنشاء منشور جديد
@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# تعديل منشور
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('home')


# حذف منشور
@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')


# تسجيل المستخدم الجديد
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# تسجيل الدخول
def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/signin.html', {'form': form})


# تسجيل الخروج
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signin')


# عرض الصفحة الشخصية
@login_required
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/profile.html', {'user': request.user, 'posts': user_posts})
