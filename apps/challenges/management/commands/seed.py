import random
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
from apps.challenges.models import Challenge, ChallengeResponse, Interaction
from taggit.models import Tag


class Command(BaseCommand):
    help = 'Seed the database with initial data for Challenges app'

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()

        # Define superuser credentials using environment variables or default values
        SUPERUSER_USERNAME = 'gabriel'
        SUPERUSER_EMAIL = 'gabriel@test.com'
        SUPERUSER_PASSWORD = 'password123'

        # Clear existing data
        self.stdout.write('Deleting old data...')
        models = [Interaction, ChallengeResponse, Challenge,
                  Tag, User]  # Order matters due to FK dependencies
        for m in models:
            m.objects.all().delete()

        # Create users
        self.stdout.write('Creating users...')
        users = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password='password123'
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users.'))

        # Create superuser
        self.stdout.write('Creating superuser...')
        if not User.objects.filter(username=SUPERUSER_USERNAME).exists():
            User.objects.create_superuser(
                username=SUPERUSER_USERNAME,
                email=SUPERUSER_EMAIL,
                password=SUPERUSER_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{SUPERUSER_USERNAME}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Superuser "{SUPERUSER_USERNAME}" already exists.'))

        # Define some sample tags
        sample_tags = ['Health', 'Fitness', 'Education', 'Technology',
                       'Art', 'Travel', 'Food', 'Music', 'Science', 'Sports']

        # Create Challenges
        self.stdout.write('Creating challenges...')
        challenges = []
        for _ in range(2):
            challenge = Challenge.objects.create(
                user=random.choice(users),
                title=fake.sentence(nb_words=6),
                description=fake.paragraph(nb_sentences=5),
                end_time=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                # image is optional; skipping for seed
            )
            # Assign random tags
            challenge.tags.add(
                *random.sample(sample_tags, k=random.randint(1, 3)))
            challenges.append(challenge)
        self.stdout.write(self.style.SUCCESS(
            f'Created {len(challenges)} challenges.'))

        # Create ChallengeResponses
        self.stdout.write('Creating challenge responses...')
        responses = []
        for challenge in challenges:
            num_responses = random.randint(1, 2)
            for _ in range(num_responses):
                response = ChallengeResponse.objects.create(
                    challenge=challenge,
                    user=random.choice(users),
                    title=fake.sentence(nb_words=6),
                    description=fake.paragraph(nb_sentences=5),
                    # image is optional; skipping for seed
                )
                # Assign random tags
                response.tags.add(
                    *random.sample(sample_tags, k=random.randint(1, 3)))
                responses.append(response)
        self.stdout.write(self.style.SUCCESS(
            f'Created {len(responses)} challenge responses.'))

        # Create Interactions
        self.stdout.write('Creating interactions...')
        interaction_types = [choice[0]
                             for choice in Interaction.INTERACTION_CHOICES]
        interactions = []
        # To track unique (response, user, interaction_type) tuples
        existing_interactions = set()

        for response in responses:
            # Determine all possible (user, interaction_type) combinations for this response
            possible_combinations = [(user, itype)
                                     for user in users for itype in interaction_types]
            # Shuffle to randomize the selection
            random.shuffle(possible_combinations)

            # Decide how many interactions to create for this response
            max_possible = len(possible_combinations)
            # Ensure we don't exceed possible combinations
            num_interactions = random.randint(1, min(10, max_possible))

            created = 0
            for user, itype in possible_combinations:
                if created >= num_interactions:
                    break
                key = (response.id, user.id, itype)
                if key not in existing_interactions:
                    interaction = Interaction.objects.create(
                        response=response,
                        user=user,
                        interaction_type=itype,
                        # celery_task_id is optional; skipping for seed
                    )
                    interactions.append(interaction)
                    existing_interactions.add(key)
                    created += 1
            # Optionally, log if unable to create desired number of interactions
            if created < num_interactions:
                self.stdout.write(
                    self.style.WARNING(
                        f"Only created {created} interactions for response ID {
                            response.id} due to uniqueness constraints."
                    )
                )

        self.stdout.write(self.style.SUCCESS(
            f'Created {len(interactions)} interactions.'))

        # Assign winning responses randomly
        self.stdout.write('Assigning winning responses...')
        for challenge in challenges:
            possible_winners = challenge.challengeresponse_set.all()
            if possible_winners.exists():
                winning_response = random.choice(possible_winners)
                challenge.winning_response = winning_response
                challenge.save()
        self.stdout.write(self.style.SUCCESS('Assigned winning responses.'))

        self.stdout.write(self.style.SUCCESS(
            'Database seeding completed successfully.'))
