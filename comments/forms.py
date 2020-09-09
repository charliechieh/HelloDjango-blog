from django import forms
from .models import Comment


class CommentFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'email': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'url': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'text': forms.widgets.Textarea(attrs={'class': 'form-control', 'rows': "4"})
        }
