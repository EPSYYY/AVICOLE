from django import forms
from .models import Product
from users.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'type', 'image', 'details_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'details_image': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        
        # Restrict product types based on user role
        if self.user and self.user.role == User.ALFISSEN:
            self.fields['type'].choices = [(Product.ALIMENTS, 'Aliments Composés')]
        elif self.user and self.user.role == User.OUAKKAHA:
            self.fields['type'].choices = [(Product.POUSSINS, 'Poussins')] 