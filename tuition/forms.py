from django import forms
from.models import Tuition,ApplyTuition

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