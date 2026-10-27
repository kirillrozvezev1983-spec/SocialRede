from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from .forms import RegisterForm, PostForm


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed/home.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if User.objects.filter(username=data['username']).exists():
                form.add_error('username', 'Этот логин уже занят.')
            else:
                user = User.objects.create_user(username=data['username'], password=data['password'], first_name=data['name'])
                Profile.objects.create(user=user, age=data['age'], work=data['work'], hobbies=data['hobbies'])
                login(request, user)
                return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'feed/register.html', {'form': form})


def user_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        error = 'Неверный логин или пароль.'
    return render(request, 'feed/login.html', {'error': error})


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile')
    else:
        form = PostForm()
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    profile_data, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'feed/profile.html', {'form': form, 'posts': posts, 'profile_data': profile_data})

@login_required
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def guest(request, username):
    person = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=person).order_by('-created_at')
    profile_data, created = Profile.objects.get_or_create(user=person)
    return render(request, 'feed/guest.html', {'person': person, 'posts': posts, 'profile_data': profile_data})
