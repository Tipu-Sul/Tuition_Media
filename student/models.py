from django.db import models
from django.contrib.auth.models import User
from. constant import GENDER,STAR
from teacher.models import Teacher

# Create your models here.

class StudentClass(models.Model):
    class_name = models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)
    def __str__(self):
        return self.class_name

class Student(models.Model):
    user=models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    image=models.ImageField(upload_to='student/images/',null=True, blank=True)
    mobile_no=models.CharField(max_length=12)
    gender=models.CharField(max_length=30,choices=GENDER)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class TuitionReview(models.Model):
    tuition=models.ForeignKey('tuition.Tuition', related_name="review", on_delete=models.CASCADE)
    teacher_id=models.IntegerField(null=True,blank=True)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField(null=True, blank=True)
    star=models.CharField(max_length=50,choices=STAR,null=True,blank=True)
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'review by{self.name}'