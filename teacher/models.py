from django.db import models
from django.contrib.auth.models import User

# Create your models here.

GENDER=(
    ("Male","Male"),
    ("Female","Female"),
)
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='teacher/images/')
    gender=models.CharField(max_length=30,choices=GENDER)
    mobile_no=models.CharField(max_length=12)
    degree=models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
