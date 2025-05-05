from django.core.management.base import BaseCommand
from authentication.models import User
from client_auth.models import Trainee
from trainer_auth.models import Trainer, Comment
from mentorship.models import Mentorship
from tests.models import Test
from notification.models import Notification
from workout.models import WorkoutPlan, WorkoutExercise
from exercise.models import Exercise
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
        trainees = []
        trainers = [] 

        profile_pictures_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        available_pictures = [f for f in os.listdir(profile_pictures_dir) 
                            if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        first_names=["سیانور", "معین", "محمدمهدی", "نازنین", "علی", "حبیب", "ایمان", "هلیا", "فرزان", "داکتر"]
        last_names=["ساختمان دار", "اکبری", "داستان دوست", "کیبوردی", "موفاسا", "قاشق فر", "قادیکلائی شهمیرزادی الاصل", "میرزاقاسمی دوست", "آدامس فر", "مَک مَکِنا"]
        
        for i in range(count):
            # Create a user
            username = f"trainee{i+1}"
            email = f"trainee{i+1}@example.com"
            password = username  # You might want to make this more secure
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
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
            trainees.append(trainee)
            test = Test.objects.create(
                trainee=trainee,
                birth_date= f"{random.randint(1990, 2005)}-{random.randint(1, 12)}-{random.randint(1, 28)}",
                weight=random.uniform(50, 100),
                height=random.uniform(150, 200),
                goal_weight=random.uniform(50, 100),
                goal=random.choice(["lose_weight", "gain_muscle", "stay_fit"]),
                equipment=random.choice(["gym", "home", "outdoor"]),
                workout_days=random.choice(["morning", "evening", "afternoon"]),
                diseases=random.choice(["diabetes", "hypertension", "obesity", "none"]),
                focus_area=random.choice(["arms", "legs", "core", "back", "chest", "full_body"]),
                fitness_level=random.randint(1, 6)
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} mock trainees')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} mock tests')
        )

        
        for i in range(count):
            # Create a user
            username = f"trainer{i+1}"
            email = f"trainer{i+1}@example.com"
            password = username  # You might want to make this more secure
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
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
                user=user,
                price=random.uniform(100000, 1000000),
                isAvailableForReservation=random.choice([True, False]),
                experience=random.randint(1, 15),
                specialties=random.choice(["قدرتی", "هوازی", "کششی", "استقامتی"]),
                certificates=random.choice(["تربیت مدرس", "خواستگاه مغول", "زابل بابل", "یورک شایر"]),
                bio=random.choice(["من یک تربیت مدرس هستم", "من یک خواستگاه مغول هستم", "من یک زابل بابل هستم", "من یک سرپرست یورک شایر هستم"]),
            )
            trainers.append(trainer)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} mock trainers')
        )

        for i in range(count * 6):
            rating=random.randint(1,5) * 1.0 + random.randint(0,9) * 0.1
            comment = "او عالی است حتما نصب کنید!" if rating > 2.5 else "او مرا به قتل رساند، خانواده من در حال طی کردن روند دادگستری برای شکایت از او هستند!"
            Comment.objects.create(
                trainee=trainees[random.randint(1,count)-1],
                trainer=trainers[random.randint(1,count)-1],
                rating=rating,
                comment=comment
            )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {6 * count} reviews')
        )


        for i in range(int(count * 3 / 4)):
            m = Mentorship.objects.create(
                trainee=trainees[i],
                trainer=trainers[i]
            )
            w = WorkoutPlan.objects.create(
                mentorship=m,
                name=f"workout{i+1}",
                description=f"از برنامت لذت ببر!",
                status=random.choice(["تمام شده", "در حال انجام", "شروع نشده"])
            )
            for j in range(random.randint(1, 5)):
                WorkoutExercise.objects.create(
                    workout_plan=w,
                    exercise=Exercise.objects.get(id=random.randint(1, int(Exercise.objects.count() * 0.8))),
                    sets=random.randint(1, 5),
                    reps=random.randint(1, 10),
                    order=j
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {int(count * 3 / 4)} mock mentorships & notifications')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {int(count * 3 / 4)} mock workout plans & workout exercises')
        )