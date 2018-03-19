from django import forms

from .models import Post
from .models import InstabotDjangoModel

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class PostInstabotDjangoModel(forms.ModelForm):

    class Meta:
        model = InstabotDjangoModel
        fields = ('login', 'password',)
