from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates default products for poussins and aliments composés'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating default products...')
        
        try:
            # Get the default users
            alfissen_user = User.objects.get(username='alfissen')
            ouakkaha_user = User.objects.get(username='ouakkaha')
            
            with transaction.atomic():
                # Create poussins products
                poussins_products = [
                    'Poulet Roux Fonce',
                    'Poulet Roux',
                    'Poulet Beldi ouakkaha',
                    'Poulet Cou Nu',
                    'Poulet Gris barre',
                    'Poulet de chair'
                ]
                
                for name in poussins_products:
                    product, created = Product.objects.get_or_create(
                        name=name,
                        defaults={
                            'description': f'Description for {name}',
                            'price': 50.0,  # Default price
                            'stock': 100,   # Default stock
                            'type': Product.POUSSINS,
                            'seller': ouakkaha_user
                        }
                    )
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created poussin product: {name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Poussin product already exists: {name}'))
                
                # Create aliments composés products
                aliments_categories = {
                    'Volailles': [
                        'Aliments Poussin Démarrage A13',
                        'Aliment Pré-Démarrage Pre-13',
                        'Aliments Poussin Croissance A23',
                        'Aliment Poulet Pré-Abattage A43',
                        'Aliment Poule Pondeuse P 64',
                        'Aliment Concentre Poulet De Chair Cdcf 43%',
                        'Aliment Concentre Poule Pondeuse Ponte 44% Cc P204',
                        'Aliments Pondeuse Et Reproductrice – PR64'
                    ],
                    'Bovins': [
                        'Aliments Veaux Démarrage JBIO',
                        'Aliments Jeunes Bovins Engraissement JB2O',
                        'Aliments Bovins Top Engraissement JB3O',
                        'Aliments Bovins Finition JB4O',
                        'Aliments Génisse En Croissance GIO',
                        'Aliments Vache Laitière 2L – VL20',
                        'Aliments Vache Laitière 2.5L – VL25',
                        'Aliments Vache Laitière 3L – VL30'
                    ],
                    'Ovins': [
                        'Aliments Agneaux d\'Engraissement O2O',
                        'Aliments Ovins Finition O3O',
                        'Aliments Brebis Gestante O4O',
                        'Aliments Brebis Allaitante O5O'
                    ]
                }
                
                for category, products in aliments_categories.items():
                    for name in products:
                        product, created = Product.objects.get_or_create(
                            name=name,
                            defaults={
                                'description': f'{category} - {name}',
                                'price': 200.0,  # Default price
                                'stock': 50,     # Default stock
                                'type': Product.ALIMENTS,
                                'seller': alfissen_user
                            }
                        )
                        
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Created aliment product: {name} (Category: {category})'))
                        else:
                            self.stdout.write(self.style.WARNING(f'Aliment product already exists: {name} (Category: {category})'))
                
            self.stdout.write(self.style.SUCCESS('Default products setup completed!'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Default users not found. Please run setup_default_users first.'))
            return 