import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from.models import Categories, SpentModel
import string


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


class RegisrtaeForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2' )



class CreateCategory(forms.Form):
    title = forms.CharField(max_length=50)

    def clean_title(self):
        title_for_validation = self.cleaned_data['title']
        if not re.match(r'[^0-9][a-z]', title_for_validation):
            raise ValidationError("Category cant start with a number")
        return title_for_validation



class CreateSpentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        q_id = kwargs.pop('q_id')
        super(CreateSpentForm, self).__init__(*args, **kwargs)
        if q_id:
            choices = []
            counter = 1
            for item in Categories.objects.filter(user=q_id):
                a = [item, item.title]
                choices.append(tuple(a))
                counter +=1
            self.fields['category'].choices = choices

    title= forms.CharField(max_length=50)
    amount = forms.FloatField()
    price_for_unit = forms.FloatField()
    comment = forms.CharField(widget=forms.Textarea())
    category = forms.ChoiceField()
