from django.db import models
from teacher.models import Teacher
from student.constant import STATUS
from django.contrib.auth.models import User
# Create your models here.
class TuitionSubject(models.Model):
    name=models.CharField(max_length=50)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.name)
    
class Tuition(models.Model):
    name=models.ForeignKey('student.StudentClass',on_delete=models.CASCADE)
    time=models.CharField(max_length=60)
    teacher=models.ForeignKey(Teacher,on_delete= models.CASCADE,null=True, blank=True)
    fee=models.DecimalField(decimal_places=2,max_digits=7,null=True, blank=True)
    subject=models.ForeignKey(TuitionSubject,on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return str(self.name)

class ApplyTuition(models.Model):
    student=models.ForeignKey(User, on_delete=models.CASCADE)
    class_name=models.ForeignKey('student.StudentClass', on_delete=models.CASCADE)
    subject=models.ForeignKey(TuitionSubject, on_delete=models.CASCADE, null=True, blank=True)
    tuition_status=models.CharField(max_length=50,choices=STATUS, default='pending')
    is_approved=models.BooleanField(default=False)
    def __str__(self):
        return self.student.first_name
    
class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=60)
    phone=models.CharField(max_length=14)
    address=models.CharField(max_length=150)
    comment=models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
