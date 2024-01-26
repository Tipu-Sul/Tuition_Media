from django import forms
from.models import Tuition,ApplyTuition,ContactUs

class AddTuitionForm(forms.ModelForm):
    class Meta:
        model=Tuition
        fields='__all__'

class EditTuitionForm(forms.ModelForm):
    class Meta:
        model=Tuition
        fields='__all__'

class ApplyTuitionForm(forms.ModelForm):
   class Meta:
       model=ApplyTuition
       fields=['class_name','subject']

class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields='__all__'

