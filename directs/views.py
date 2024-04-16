from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from directs.models import Message
from django.contrib.auth.decorators import login_required
from authy.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.

@login_required
def inbox(request):
    user=request.user
    messages = Message.get_message(user=request.user)

    
    active_direct = None
    directs = None
    profile = get_object_or_404(Profile,user=user)

    if messages:
        message = messages[0]
        print(message)
        active_direct = message['users'].username
        print(active_direct)
        
    
       
        directs=Message.objects.filter(user=request.user,reciepient=message['users'])
        print(directs)      # showing all messages respected users
        directs.update(is_read=True)    

        for message in messages:
             
             
             if message['users'].username == active_direct:
                 message['unread'] = 0
    
    context = {
        'directs':directs,
        'messages':messages,
        'active_direct':active_direct,
        'profile':profile,
        
        
    }
    return render(request,'directs/direct.html',context)


@login_required
def Directs(request,username):
    user=request.user
    messages = Message.get_message(user=request.user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username) 
    directs.update(is_read=True)

   

    for message in messages:
    
        if message['users'].username == username:
            message['unread'] = 0
    
    context = {
        'directs':directs,
        'messages':messages,
        'active_direct':active_direct,
       
    }
    return render(request,'directs/direct.html',context)


def SendDirect(request):
     from_user = request.user
     to_user_username = request.POST.get('to_user')
     body = request.POST.get('body')

     if request.method=='POST':
          to_user = User.objects.get(username=to_user_username)
          Message.sender_message(from_user,to_user,body)
          return redirect('message')
     


def UserSearch(request):
     query = request.GET.get('q')
     context = {}
     if query:
          users = User.objects.filter(Q(username__icontains=query))

          # Paginator 
          paginator = Paginator(users,8)
          page_number = request.GET.get('page')
          user_paginator = paginator.get_page(page_number)

          context = {
               'users':user_paginator
          }
     return render(request,'directs/search.html',context)



def NewConversation(request,username):
     from_user = request.user
     body = ''
     try:
          to_user = User.objects.get(username=username)
     except Exception as e:
          return redirect('search-users')
     if from_user != to_user:
          Message.sender_message(from_user,to_user,body)
     return redirect('message')