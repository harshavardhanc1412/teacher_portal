from django.db import models
from django.contrib.auth.models import AbstractUser

class Teacher(AbstractUser):
    pass

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('name', 'subject', 'teacher')
    
    def __str__(self):
        return f"{self.name} - {self.subject}"