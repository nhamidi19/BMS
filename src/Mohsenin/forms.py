from django import forms  
from .models import Family, Dist

class DistForm(forms.ModelForm):
    class Meta:
        model = Dist
        fields = '__all__'

class FamilyForm(forms.ModelForm):  
    class Meta:  
        model = Family  
        fields = '__all__' 

class NewFamilyForm(forms.ModelForm):  
    class Meta:  
        model = Family  
        fields = ['doc_code', 'need_level', 'family_type', 'address', 'contact_number', 'postal_code',  'is_active'] 

