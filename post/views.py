from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from authy.models import Profile
from .forms import NewPostForm
from comment.models import Comment
from comment.forms import NewCommentForm
from django.contrib.auth.decorators import login_required
from directs.models import Message
import json
from django.http import HttpResponse

# Create your views here.

@login_required
def index(request):
    user = request.user
    all_users = User.objects.all()
    # print(all_users)
    follow_status = Follow.objects.filter(following=user,follower=request.user).exists()
    profile = Profile.objects.all()
    # print(profile)
   
    
    posts = Stream.objects.filter(user=user)
    # print(posts) 

    group_ids = []
    stories=[]
    for users in StoryProfile.objects.all():
        items = []    
        for status in users.status.all():
            items.append({
                "id":status.id,
                "type":"",
                "length":3,
                "src": f'/media/{status.file}',
                

            })
        stories.append({ 
            "id":str(users.uid),
            "photo":f'/media/{users.user.profile.image}',
            "items":items,
            "name": users.user.username,

        })


    for post in posts:
        group_ids.append(post.post_id)

    # print(group_ids)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # paginator = Paginator(users,6)
        # page_number = request.GET.get('page')
        # user_paginator = paginator.get_page(page_number)

    context = {
            'post_items':post_items,
            'follow_status':follow_status,
            'all_users':all_users,
            'profile':profile,
            'stories':json.dumps(stories),
            
          
            # 'users_paginator':user_paginator,
        }
    
    return render(request,'app/index.html',context)




@login_required
def new_post(request):
    user = request.user
    profile = get_object_or_404(Profile,user=user)
    tags_objs=[]

    if request.method=='POST':
        form = NewPostForm(request.POST,request.FILES)
        if form.is_valid():
            picture = form.cleaned_data['picture']
            caption = form.cleaned_data['caption']
            tag_form = form.cleaned_data['tags']
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t,created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            p,created = Post.objects.get_or_create(picture=picture,caption=caption,user=user)
            p.tags.set(tags_objs)
            p.save()
            return redirect('profile',request.user.username)
    else:
        form = NewPostForm()
        
    context = {
            'form':form
        }
            
    return render(request,'app/newpost.html',context)



@login_required
def post_detail(request,post_id):
    user = request.user
    post = get_object_or_404(Post,id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details',args=[post.id]))

    else:
        form = NewCommentForm()
    
    context = {
        'post':post,
        'form':form,
        'comments':comments
    }
        
    return render(request,'app/postdetail.html',context)



@login_required
def tags(request,tag_slug):
    tag = get_object_or_404(Tag,slug=tag_slug)
   
    posts = Post.objects.filter(tags=tag).order_by('-posted')
    context = {
        'posts':posts,
        'tag':tag
    }
    return render(request,'app/tag.html',context)




@login_required
def like(request,post_id):
    user = request.user 
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user,post=post).count()

    if not liked:
        Likes.objects.create(user=user,post=post)
        current_likes += 1
    else:
        Likes.objects.filter(user=user,post=post).delete()
        current_likes -= 1

    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('post-details',args=[post.id]))



@login_required
def favourite(request,post_id):
    user = request.user 
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        Profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details',args=[post.id]))



    


def add_story(request):
    user = StoryProfile.objects.get(user_id=request.user)
    print(user)
    if request.method=='POST':
        
        story = request.FILES.get('story')
        user_story = Story.objects.create(user=user,file=story)
        return redirect('index')
        
     
    
   
    return render(request,'app/add_story.html',{'user':user})




