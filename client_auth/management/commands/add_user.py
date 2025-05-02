from django.core.management.base import BaseCommand
from authentication.models import User
from client_auth.models import Trainee
from trainer_auth.models import Trainer
import random
import os
from django.core.files import File
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates mock trainees & trainers with random data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of mock trainees & trainers to create (default: 50)'
        )

    def handle(self, *args, **options):
        count = options['count']

        profile_pictures_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        available_pictures = [f for f in os.listdir(profile_pictures_dir) 
                            if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        for i in range(count):
            # Create a user
            username = f"trainee{i+1}"
            email = f"trainee{i+1}@example.com"
            password = username  # You might want to make this more secure

            first_name=random.choice(["سیانور", "معین", "محمدمهدی", "نازنین", "علی", "حبیب", "ایمان", "کشکساناز", "گارفیلد", "داکتر"]),
            last_name=random.choice(["چوب زاده", "ناشتا", "کله بامشی", "خی زاده", "زیانزاده", "قاشق فر", "قادیکلائی شهمیرزادی الاصل", "میرزاقاسمی دوست", "آدامس فر", "قندیل خور"]),
            name = f"{first_name} {last_name}"

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                name = name
            )

            if available_pictures:
                random_picture = random.choice(available_pictures)
                picture_path = os.path.join(profile_pictures_dir, random_picture)
                with open(picture_path, 'rb') as f:
                    user.profile_picture.save(
                        f'{username}_{random_picture}',
                        File(f),
                        save=True
                    )
            
            # Create trainee profile
            trainee = Trainee.objects.create(
                user=user,
                height=random.uniform(150, 200),  # Random height between 150-200 cm
                weight=random.uniform(50, 100)    # Random weight between 50-100 kg
            )


        
        for i in range(count):
            # Create a user
            username = f"trainer{i+1}"
            email = f"trainer{i+1}@example.com"
            password = username  # You might want to make this more secure

            first_name=random.choice(["سیانور", "معین", "محمدمهدی", "نازنین", "علی", "حبیب", "ایمان", "محمدحسین", "گارفیلد", "داکتر"]),
            last_name=random.choice(["چوب زاده", "ناشتا", "کله بامشی", "خی زاده", "زیانزاده", "قاشق فر", "قادیکلائی شهمیرزادی الاصل", "میرزاقاسمی دوست", "آدامس فر", "قندیل خور"]),
            name = f"{first_name} {last_name}"

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                name = name
            )

            if available_pictures:
                random_picture = random.choice(available_pictures)
                picture_path = os.path.join(profile_pictures_dir, random_picture)
                with open(picture_path, 'rb') as f:
                    user.profile_picture.save(
                        f'{username}_{random_picture}',
                        File(f),
                        save=True
                    )
            
            # Create trainer profile
            trainer = Trainer.objects.create(
                user=user
            )
        


        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} mock trainees & trainers')
        ) 