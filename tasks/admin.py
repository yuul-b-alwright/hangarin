from django.contrib import admin
from .models import Priority, Category, Task

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'category', 'deadline', 'is_completed')
    list_filter = ('is_completed', 'priority', 'category')
    search_fields = ('title',)