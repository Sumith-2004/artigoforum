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
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text="You can update your username here. It must be unique."
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'profile_picture', 'bio']  # Replace 'user' with 'username'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username  # Pre-fill with current username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username

    def save(self, commit=True):
        profile = super().save(commit=False)
        username = self.cleaned_data.get('username')
        if profile.user.username != username:
            profile.user.username = username
            profile.user.save()
        if commit:
            profile.save()
        return profile
