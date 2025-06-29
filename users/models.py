from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 'admin'
    ALFISSEN = 'alfissen'
    OUAKKAHA = 'ouakkaha'
    CUSTOMER = 'customer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (ALFISSEN, 'Alfissen'),
        (OUAKKAHA, 'Ouakkaha'),
        (CUSTOMER, 'Customer'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
        
    @property
    def is_alfissen(self):
        return self.role == self.ALFISSEN
        
    @property
    def is_ouakkaha(self):
        return self.role == self.OUAKKAHA
        
    @property
    def is_customer(self):
        return self.role == self.CUSTOMER
