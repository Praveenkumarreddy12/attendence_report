from django.db import models

# Create your models here.
class Register(models.Model):
    emo_name = models.CharField(max_length=100)
    empid = models.CharField(max_length=100)
    emp_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='images/')


