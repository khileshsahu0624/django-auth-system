from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):    # dunder method
        return self.name