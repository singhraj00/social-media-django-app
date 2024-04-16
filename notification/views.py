from django.shortcuts import render,redirect
import imp
from  notification.models import Notification

# Create your views here.


def ShowNotification(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    print(notifications)

    context = {
        'notifications':notifications,
    }
    return render(request,'notification/notification.html',context)


def DeleteNotification(request,noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id,user=user).delete()
    return redirect('show-notification')