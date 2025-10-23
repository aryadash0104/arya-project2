# forms.py
from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'city', 'contact_number', 'bio', 'gender']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        instance = super(ProfileForm, self).save(commit=False)
        
        if instance.user:
            user = instance.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.save()

        if commit:
            instance.save()

        return instance
