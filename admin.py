from django.contrib import admin
from .models import Priority, Category, Task, SubTask, Note

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Display specific fields [cite: 165]
    list_display = ('title', 'status', 'deadline', 'priority', 'category')
    # Add filters [cite: 166]
    list_filter = ('status', 'priority', 'category')
    # Enable search [cite: 167]
    search_fields = ('title', 'description')

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'parent_task_name')
    list_filter = ('status',)
    search_fields = ('title',)

    # Custom field to display parent task name [cite: 169, 170]
    def parent_task_name(self, obj):
        return obj.parent_task.title

@admin.register(Category, Priority)
class SimpleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('task', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
    
# tasks/admin.py

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'priority', 'category')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description')
    
    # This line "injects" your custom CSS into the Admin HTML
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }