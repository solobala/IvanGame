from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#


class NewUserForm(UserCreationForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    link = forms.URLField()
    owner_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email",  "password1", "password2"]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


