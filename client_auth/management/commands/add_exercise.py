from django.core.management.base import BaseCommand
from authentication.models import User
from exercise.models import ExerciseTag, MuscleGroup, Equipment, Exercise, ExerciseImage
import random
import os
from django.core.files import File
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates mock exercises with random data and images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of mock exercises to create (default: 50)'
        )
        parser.add_argument(
            '--images-per-exercise',
            type=int,
            default=1,
            help='Number of images to add per exercise (default: 1)'
        )

    def handle(self, *args, **options):
        count = options['count']
        images_per_exercise = options['images_per_exercise']

        exercise_images_dir = os.path.join(settings.MEDIA_ROOT, 'exercise_images')
        available_pictures = [f for f in os.listdir(exercise_images_dir) 
                            if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not available_pictures:
            self.stdout.write(
                self.style.WARNING('No exercise images found in media/exercise_images/')
            )
        
        exercise_tags = ['کششی', 'استقامتی', 'هوازی', 'قدرتی', 'فانکشنال']
        muscle_groups = ['سرشانه', 'پا', 'شکم و پهلو', 'سینه', 'زیر بغل']
        equipments = ['استپ', 'کش', 'شیش', 'هالتر', 'دمبل', 'نیمکت']

        # Create tags, muscle groups, and equipment if they don't exist
        for t in exercise_tags:
            ExerciseTag.objects.get_or_create(name=t)
        
        for m in muscle_groups:
            MuscleGroup.objects.get_or_create(name=m)
        
        for e in equipments:
            Equipment.objects.get_or_create(name=e)
        
        for i in range(count):
            # Create a user
            exercise_name = f"تمرین {i+1}"
            description = f"این تمرین {i+1} برای تقویت {random.choice(muscle_groups)} است"
            difficulty = random.choice(['مبتدی', 'متوسط', 'پیشرفته'])
            workoutplaces = random.choice(['باشگاه', 'خانه'])
            
            exercise = Exercise.objects.create(
                name=exercise_name,
                description=description,
                difficulty=difficulty,
                workoutplaces=workoutplaces
            )
            
            # Add random tags, muscle groups, and equipment
            exercise.tags.set(random.sample(list(ExerciseTag.objects.all()), random.randint(1, len(exercise_tags))))
            exercise.muscle_groups.set(random.sample(list(MuscleGroup.objects.all()), random.randint(1, len(muscle_groups))))
            exercise.equipments.set(random.sample(list(Equipment.objects.all()), random.randint(1, len(equipments))))
            
            # Add random images if available
            if available_pictures:
                # Select random images for this exercise
                selected_images = random.sample(available_pictures, min(images_per_exercise, len(available_pictures)))
                for img in selected_images:
                    picture_path = os.path.join(exercise_images_dir, img)
                    with open(picture_path, 'rb') as f:
                        ExerciseImage.objects.create(
                            exercise=exercise,
                            image=File(f, name=f'exercise_{exercise.id}_{img}')
                        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} mock exercises')
        ) 