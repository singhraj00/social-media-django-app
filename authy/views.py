from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Profile
from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from authy.models import Profile
from .forms import EditProfileForm, UserRegistrationForm
from django.urls import resolve
from comment.models import Comment



def UserProfile(request,username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User,username=username)
    profile =Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()

    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follower_count = Follow.objects.filter(following=user).count()

    follow_status = Follow.objects.filter(following=user,follower=request.user).exists()
    print(follow_status)

    context = {
        'posts':posts,
        'profile':profile,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':follower_count,
        'follow_status':follow_status
    }

    return render(request,'authy/profile.html',context)



def editProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.loaction = form.cleaned_data.get('loaction')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile',profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)
    context = {
        'form':form,
    }

    return render(request,'authy/editprofile.html',context)


def follow(request,username,option):
    user = request.user
    following = get_object_or_404(User,username=username)
    print(following)


    try:
        f, created = Follow.objects.get_or_create(follower=request.user,following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following,user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post,user=request.user,date=post.posted,following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile',args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile',args=[username]))



def register(request):
    if request.method=='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Congratulations, your account was created !')

            # automatically login 
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
            login(request,new_user)
            return redirect('index')
        
    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form
    }

    return render(request,'authy/sign-up.html',context)
    
