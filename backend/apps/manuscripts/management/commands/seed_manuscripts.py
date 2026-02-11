"""
Management command to seed test manuscripts.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.manuscripts.models import Manuscript, Surrogate
import uuid

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample manuscripts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of manuscripts to create',
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Username of user to create manuscripts for (creates user if not exists)',
        )

    def handle(self, *args, **options):
        count = options['count']
        username = options.get('user', 'admin')

        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {username} (password: admin123)')
            )
        else:
            self.stdout.write(f'Using existing user: {username}')

        # Sample manuscript data
        sample_manuscripts = [
            {
                'shelfmark': 'MS. Bodl. 264',
                'repository': 'Bodleian Library',
                'collection': 'Bodley',
                'material': 'parchment',
                'folios': 220,
                'date_earliest': 1330,
                'date_latest': 1340,
                'date_display': 'c. 1330-1340',
                'origin_location': 'England',
                'language': 'Latin',
                'script': 'Gothic',
                'content_summary': 'Roman de la Rose with extensive heraldic decoration',
            },
            {
                'shelfmark': 'Royal MS 2 B VII',
                'repository': 'British Library',
                'collection': 'Royal',
                'material': 'parchment',
                'folios': 180,
                'date_earliest': 1300,
                'date_latest': 1320,
                'date_display': 'early 14th century',
                'origin_location': 'France',
                'language': 'French',
                'script': 'Gothic',
                'content_summary': 'Psalter with heraldic borders',
            },
            {
                'shelfmark': 'Add. MS 42130',
                'repository': 'British Library',
                'collection': 'Additional',
                'material': 'parchment',
                'folios': 95,
                'date_earliest': 1400,
                'date_latest': 1420,
                'date_display': 'c. 1400-1420',
                'origin_location': 'Burgundy',
                'language': 'Latin',
                'script': 'Gothic',
                'content_summary': 'Book of Hours with coats of arms',
            },
            {
                'shelfmark': 'W. 45',
                'repository': 'Walters Art Museum',
                'collection': 'Manuscripts',
                'material': 'parchment',
                'folios': 156,
                'date_earliest': 1350,
                'date_latest': 1370,
                'date_display': 'mid-14th century',
                'origin_location': 'Flanders',
                'language': 'Latin',
                'script': 'Gothic',
                'content_summary': 'Breviary with heraldic initials',
            },
            {
                'shelfmark': 'MS Fr. 12595',
                'repository': 'Bibliothèque nationale de France',
                'collection': 'Français',
                'material': 'parchment',
                'folios': 240,
                'date_earliest': 1280,
                'date_latest': 1300,
                'date_display': 'late 13th century',
                'origin_location': 'Paris',
                'language': 'French',
                'script': 'Gothic',
                'content_summary': 'Chronique universelle with heraldic illustrations',
            },
        ]

        created_count = 0
        for i, data in enumerate(sample_manuscripts[:count]):
            manuscript, created = Manuscript.objects.get_or_create(
                shelfmark=data['shelfmark'],
                repository=data['repository'],
                defaults={
                    **data,
                    'created_by': user,
                    'dimensions': {
                        'height': 280 + i * 10,
                        'width': 200 + i * 5,
                        'unit': 'mm'
                    },
                    'bibliography': [
                        f"Reference {i+1}",
                        f"Another reference {i+1}",
                    ],
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created manuscript: {manuscript.shelfmark}')
                )
            else:
                self.stdout.write(f'Skipped existing manuscript: {manuscript.shelfmark}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} new manuscript(s)'
            )
        )

