from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm

# عرض الصفحة الرئيسية مع كل المنشورات
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

# تسجيل الدخول
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'blog/login.html', {'error': 'Invalid credentials'})
    return render(request, 'blog/login.html')

# تسجيل الخروج
def user_logout(request):
    logout(request)
    return redirect('login')

# إنشاء حساب جديد
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        return render(request, 'blog/signup.html', {'form': form})

# عرض صفحة المستخدم الشخصية
@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/profile.html', {'posts': posts})

# إنشاء منشور جديد
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile')
    else:
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})

# تعديل منشور موجود
@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_form.html', {'form': form})

# حذف منشور
@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})