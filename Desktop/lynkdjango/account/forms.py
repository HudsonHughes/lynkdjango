from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django import forms
from django.contrib.auth.models import User
# get a way to log the errors:
import logging
log = logging.getLogger(__name__)
# convert the errors to text
from django.utils.encoding import force_text


class UserCreationForm(BaseUserCreationForm):
    # declare the fields you will show
    username = forms.CharField(label="Your Username")
    email = forms.EmailField(label="Email Address")
    first_name = forms.CharField(label="Name")
    middle_name = forms.CharField(label="Middle Name", required=False)
    last_name = forms.CharField(label="Surname")

    # this sets the order of the fields
    class Meta:
        model = User
        fields = ("first_name", "middle_name", "last_name", "email", "username", "password1", "password2",)

    # this redefines the save function to include the fields you added
    def save(self, commit=True):
        print("attempting ")
        user = super(BaseUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.middle_name = self.cleaned_data["middle_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user