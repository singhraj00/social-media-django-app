from django import forms  
from django.contrib.auth.models import User
from .models import Comment


class NewCommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Write comment'}),required=True)

    class Meta:
        model = Comment
        fields = ('body',)