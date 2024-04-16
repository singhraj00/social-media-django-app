from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from authy.views import UserProfile,editProfile,follow,register
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm,PasswordChangeForm

urlpatterns = [
    path('profile/<slug:username>/',UserProfile,name='profile'),
    
    path('profile/edit',editProfile,name='editprofile'),
    path('<username>/follow/<option>/',follow,name='follow'),
    path('',register,name='sign-up'),
    path('sign-in/',auth_views.LoginView.as_view(template_name='authy/sign-in.html',redirect_authenticated_user=True),name='sign-in'),
    path('sign-out/',auth_views.LogoutView.as_view(template_name='authy/sign-out.html'),name='sign-out'),
    path('reset-password/',auth_views.PasswordResetView.as_view(template_name='authy/password_reset.html',form_class=PasswordResetForm),name='password-reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='authy/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='authy/password_reset_confirm.html',form_class=SetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='authy/password_reset_complete.html'),name='password_reset_complete'),
    path('password-change/',auth_views.PasswordChangeView.as_view(template_name='authy/passwordchange.html',form_class=PasswordChangeForm,success_url='/password-change-done/'),name='password-change-form'),
    path('password-change-done/',auth_views.PasswordChangeDoneView.as_view(template_name='authy/passwordchangedone.html'),name='password-change-done'),
]