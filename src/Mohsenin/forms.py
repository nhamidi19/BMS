from django import forms  
from .models import Family  

class FamilyForm(forms.ModelForm):  
    class Meta:  
        model = Family  
        fields = '__all__' 

class NewFamilyForm(forms.ModelForm):  
    class Meta:  
        model = Family  
        fields = ['doc_code', 'need_level', 'family_type', 'address', 'contact_number', 'postal_code',  'is_active'] 