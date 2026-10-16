from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="students"
    )
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    age = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name="students")
    marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name