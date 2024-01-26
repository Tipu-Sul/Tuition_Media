from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from. models import Teacher

GENDER=(
    ("Male","Male"),
    ("Female","Female"),
)


class TeacherRegistrationForm(UserCreationForm):
    image=forms.ImageField()
    mobile_no=forms.CharField()
    degree=forms.CharField()
    gender=forms.ChoiceField(choices=GENDER)
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','image', 'mobile_no','degree', 'gender']
    
  
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
            Teacher.objects.create(
                user=user,
                image=self.cleaned_data.get('image'),
                mobile_no=self.cleaned_data.get('mobile_no'),
                gender=self.cleaned_data.get('gender'),
                degree=self.cleaned_data.get('degree'),
            )
        return user