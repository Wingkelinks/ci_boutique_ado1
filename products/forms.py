from django import forms
from .models import Product, Category 

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # overide init method to make changes to fields
        categories = Category.objects.all() 
        # get all categories and
        # create list of tuples of friendly names associated with category ids
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
        