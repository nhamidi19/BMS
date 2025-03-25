from django import forms  
from .models import *

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

class NewPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["first_name", "last_name", "father_name", "national_id", "birth_date", "is_orphan", "is_guardian"]


class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ["agent_name", "observation_date", "notes"]

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = "__all__"

class PackageDistributionForm(forms.ModelForm):
    class Meta:
        model = PackageDistribution
        fields = "__all__"


class MedicalAidForm(forms.ModelForm):
    class Meta:
        model = MedicalAid
        fields = "__all__"