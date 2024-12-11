from django.db import models

# Create your models here.
class Register(models.Model):
    emo_name = models.CharField(max_length=100)
    empid = models.CharField(max_length=100, primary_key=True)
    emp_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to='images/' , null=True, blank=True)
    total_days = models.IntegerField(default=0)

    def __str__(self):
        return self.empid

class Attendence(models.Model):
    empid = models.CharField(max_length=100)
    uploadedat = models.DateTimeField(auto_now_add=True)



