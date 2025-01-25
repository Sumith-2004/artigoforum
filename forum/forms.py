from django import forms 
from .models import *

# Forms for the models
class ArtworkForm(forms.ModelForm): 
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image', 'tags']
        widgets ={
            'description' : forms.Textarea(attrs={'rows':5}),
            'tags' : forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={'rows':3, })
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
            'bio' : forms.Textarea(attrs={'rows':4})
        }

