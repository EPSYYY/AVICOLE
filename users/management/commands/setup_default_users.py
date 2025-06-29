from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates default users for admin, alfissen, and ouakkaha roles'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating default users...')
        
        with transaction.atomic():
            # Create admin user if it doesn't exist
            if not User.objects.filter(username='admin').exists():
                admin_user = User.objects.create_superuser(
                    username='admin',
                    email='admin@avicole.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User',
                    role='admin'
                )
                self.stdout.write(self.style.SUCCESS(f'Admin user created: {admin_user.username}'))
            else:
                self.stdout.write(self.style.WARNING('Admin user already exists'))
            
            # Create alfissen user if it doesn't exist
            if not User.objects.filter(username='alfissen').exists():
                alfissen_user = User.objects.create_user(
                    username='alfissen',
                    email='alfissen@avicole.com',
                    password='alfissen123',
                    first_name='Alfissen',
                    last_name='User',
                    role='alfissen'
                )
                self.stdout.write(self.style.SUCCESS(f'Alfissen user created: {alfissen_user.username}'))
            else:
                self.stdout.write(self.style.WARNING('Alfissen user already exists'))
            
            # Create ouakkaha user if it doesn't exist
            if not User.objects.filter(username='ouakkaha').exists():
                ouakkaha_user = User.objects.create_user(
                    username='ouakkaha',
                    email='ouakkaha@avicole.com',
                    password='ouakkaha123',
                    first_name='Ouakkaha',
                    last_name='User',
                    role='ouakkaha'
                )
                self.stdout.write(self.style.SUCCESS(f'Ouakkaha user created: {ouakkaha_user.username}'))
            else:
                self.stdout.write(self.style.WARNING('Ouakkaha user already exists'))
        
        self.stdout.write(self.style.SUCCESS('Default users setup completed!')) 