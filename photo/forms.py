from django import forms
from django.contrib.auth.models import User

from .models import Album, Picture


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['album_title', 'album_logo']


class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['pic_title','pic_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
