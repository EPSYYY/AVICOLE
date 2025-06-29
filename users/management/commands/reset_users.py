from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes all existing users and creates only the default users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force deletion without confirmation',
        )

    def handle(self, *args, **kwargs):
        force = kwargs.get('force', False)
        
        if not force:
            self.stdout.write(self.style.WARNING('WARNING: This will delete ALL existing users!'))
            self.stdout.write('Are you sure you want to continue? [y/N]: ')
            user_input = input().lower()
            if user_input != 'y':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return
        
        with transaction.atomic():
            # Delete all existing users
            user_count = User.objects.all().count()
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {user_count} existing users'))
            
            # Create admin user
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@avicole.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))
            
            # Create alfissen user
            alfissen_user = User.objects.create_user(
                username='alfissen',
                email='alfissen@avicole.com',
                password='alfissen123',
                first_name='Alfissen',
                last_name='User',
                role='alfissen'
            )
            self.stdout.write(self.style.SUCCESS(f'Created alfissen user: {alfissen_user.username}'))
            
            # Create ouakkaha user
            ouakkaha_user = User.objects.create_user(
                username='ouakkaha',
                email='ouakkaha@avicole.com',
                password='ouakkaha123',
                first_name='Ouakkaha',
                last_name='User',
                role='ouakkaha'
            )
            self.stdout.write(self.style.SUCCESS(f'Created ouakkaha user: {ouakkaha_user.username}'))
        
        self.stdout.write(self.style.SUCCESS('User reset completed successfully!')) 