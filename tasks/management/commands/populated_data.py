from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from tasks.models import Task, Priority, Category
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Use an existing user for generated tasks, or create a demo user.
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(username='demo', password='demo123')
            self.stdout.write(self.style.WARNING('No existing users found. Created demo user: demo/demo123'))

        # 1. Manual Priority and Category records 
        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        categories = ["Work", "School", "Personal", "Finance", "Projects"]
        
        priority_objs = [Priority.objects.get_or_create(name=p)[0] for p in priorities]
        category_objs = [Category.objects.get_or_create(name=c)[0] for c in categories]

        # 2. Generate Fake Tasks 
        for _ in range(10):
            # Requirements for title and description [cite: 115, 116, 117]
            status_choice = random.choice(["Pending", "In Progress", "Completed"])
            is_completed = status_choice == "Completed"
            task = Task.objects.create(
                user=user,
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()), # [cite: 160, 162]
                is_completed=is_completed,
                category=random.choice(category_objs),
                priority=random.choice(priority_objs)
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated data!'))