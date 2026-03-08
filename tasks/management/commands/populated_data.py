from django.core.management.base import BaseCommand
from faker import Faker
from your_app.models import Task, Priority, Category, Note, SubTask
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # 1. Manual Priority and Category records 
        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        categories = ["Work", "School", "Personal", "Finance", "Projects"]
        
        priority_objs = [Priority.objects.get_or_create(name=p)[0] for p in priorities]
        category_objs = [Category.objects.get_or_create(name=c)[0] for c in categories]

        # 2. Generate Fake Tasks 
        for _ in range(10):
            # Requirements for title and description [cite: 115, 116, 117]
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()), # [cite: 160, 162]
                status=random.choice(["Pending", "In Progress", "Completed"]),
                category=random.choice(category_objs),
                priority=random.choice(priority_objs)
            )

            # Generate Fake Notes and SubTasks 
            Note.objects.create(task=task, content=fake.paragraph())
            SubTask.objects.create(
                parent_task=task, 
                title=fake.sentence(nb_words=3),
                status=random.choice(["Pending", "In Progress", "Completed"])
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated data!'))