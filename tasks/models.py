from django.db import models
from django.contrib.auth.models import User

class Priority(models.Model):
    name = models.CharField(max_length=50) # Critical, High, Low
    def __clstr__(self): return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['deadline'] # Automatic arrangement by date