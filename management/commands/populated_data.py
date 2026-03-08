from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from tasks.models import Task, Priority, Category, Note, SubTask

class Command(BaseCommand):
    help = 'Populates the database with fake data for Hangarin App'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # 1. Ensure Priority and Category exist (Manual requirement)
        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        categories = ["Work", "School", "Personal", "Finance", "Projects"]
        
        p_objs = [Priority.objects.get_or_create(name=p)[0] for p in priorities]
        c_objs = [Category.objects.get_or_create(name=c)[0] for c in categories]

        self.stdout.write("Generating tasks...")

        # 2. Generate 10 Fake Tasks
        for _ in range(10):
            # Requirements from PDF:
            # - title: sentence(nb_words=5)
            # - description: paragraph(nb_sentences=3)
            # - deadline: timezone.make_aware(fake.date_time_this_month())
            # - status: random_element(["Pending", "In Progress", "Completed"])
            
            status_choice = fake.random_element(elements=["Pending", "In Progress", "Completed"])
            
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=status_choice,
                priority=random.choice(p_objs),
                category=random.choice(c_objs)
            )

            # 3. Create a SubTask for each task
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )

            # 4. Create a Note for each task
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated Hangarin data!'))