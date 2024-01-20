from typing import Any
from django import forms
from.constant import STUDENT_CLASS,GENDER,STAR
from. models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class StudentRegistrationForm(UserCreationForm):
    image=forms.ImageField()
    mobile_no=forms.CharField()
    gender=forms.ChoiceField(choices=GENDER)
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','image', 'mobile_no', 'gender']
    
  
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
            Student.objects.create(
                user=user,
                image=self.cleaned_data.get('image'),
                mobile_no=self.cleaned_data.get('mobile_no'),
                gender=self.cleaned_data.get('gender')
            )
        return user
    
class StudentUpdateForm(forms.ModelForm):
    image=forms.ImageField()
    mobile_no=forms.CharField()
    gender=forms.ChoiceField(choices=GENDER)
    
    class Meta:
        model=User
        fields=['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
               student=self.instance.account 
            except Student.DoesNotExist:
                student=None
            if student is not None:
                self.fields['image'].initial=student.image
                self.fields['mobile_no'].initial=student.mobile_no
                self.fields['gender'].initial=student.gender
    def save(self,commit=True):
        user=super().save(commit=False)
        if commit:
            user.save()
            student_account,created=Student.objects.get_or_create(user=user)

            student_account.image=self.cleaned_data['image']
            student_account.gender=self.cleaned_data['gender']
            student_account.mobile_no=self.cleaned_data['mobile_no']
            student_account.save()
        return user
    


class TuitionReviewForm(forms.Form):
    body=forms.CharField(widget=forms.TextInput)
    star=forms.ChoiceField(choices=STAR)
    def clean(self):
        return super().clean()
