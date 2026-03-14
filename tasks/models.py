from django.db import models
from django.contrib.auth.models import User

class Priority(models.Model):
    name = models.CharField(max_length=50) # e.g., High, Medium, Low
    
    # Fixed the typo here from __clstr__ to __str__
    def __str__(self): 
        return self.name

    class Meta:
        verbose_name_plural = "Priorities"

class Category(models.Model):
    name = models.CharField(max_length=50) # e.g., Assignment, Activity
    
    def __str__(self): 
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    # Changed to SET_NULL so deleting a category doesn't delete the task
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['is_completed', 'deadline'] # Completed tasks move to bottom