from django import forms
from .models import Post, Document

from django.utils.translation import gettext_lazy as _



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'institute']

class DocumentForm(forms.ModelForm):
    files = forms.FileField(label='첨부 파일', required=False, widget= forms.FileInput(attrs={'class': 'form'}))
    class Meta:
        model = Document
        exclude = ['attached', 'filename', 'content_type', 'size']