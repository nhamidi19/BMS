from django import forms  
from .models import Family, Dist, Person

class DistForm(forms.ModelForm):
    class Meta:
        model = Dist
        fields = '__all__'

class FamilyForm(forms.ModelForm):  
    class Meta:  
        model = Family  
        fields = ['doc_code', 'need_level', 'family_type', 'address', 'contact_number', 'postal_code',  'is_active', 'distlist'] 

class NewFamilyForm(forms.ModelForm):  
    class Meta:  
        model = Family  
        fields = ['doc_code', 'need_level', 'family_type', 'address', 'contact_number', 'postal_code',  'is_active']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person 
        fields = '__all__'

