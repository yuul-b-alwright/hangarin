from django.apps import AppConfig

class TasksConfig(AppConfig):
    # This sets the default type for primary keys (IDs) to BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'
    
    # This must match the folder name of your app
    name = 'tasks'
    
    # Optional: You can set a human-readable name for the Admin sidebar
    verbose_name = 'Hangarin Task Manager'