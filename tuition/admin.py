from typing import Any
from django.contrib import admin
from. import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Register your models here.
class TuitionSubjectAdmin(admin.ModelAdmin):
    list_display=['name','time','teacher','fee','subject']


class ApplyTuitionAdmin(admin.ModelAdmin):
    list_display=['student','class_name','tuition_status','is_approved']
    
    def student_name(self,obj):
        return obj.applytuition.student.first_name+" "+obj.applytuition.student.last_name
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.tuition_status == 'active'  and obj.is_approved==True:
            email_subject='Your request for tuition has been approved'
            email_body=render_to_string('confirm_tuition_mail.html', {'user':obj.student,'class':obj.class_name})
            email=EmailMultiAlternatives(email_subject,"",to=[obj.student.email])
            email.attach_alternative(email_body,'text/html')
            email.send()

admin.site.register(models.ApplyTuition, ApplyTuitionAdmin)
admin.site.register(models.Tuition,TuitionSubjectAdmin)
admin.site.register(models.TuitionSubject)