from django.shortcuts import render, get_object_or_404, redirect  
from django.views import View  
from django.views.generic import ListView, CreateView, UpdateView, DeleteView  
from django.urls import reverse_lazy  
from .models import Family  
from .forms import FamilyForm, NewFamilyForm

# Create your views here.

def index(request):
    return render(request, 'Mohsenin/index.html')

  # You need to create this form  

class FamilyListView(ListView):  
    model = Family  
    template_name = 'Mohsenin/family_list.html'  
    context_object_name = 'families'  


class FamilyCreateView(CreateView):  
    model = Family  
    form_class = NewFamilyForm  # Use a ModelForm for Family  
    template_name = 'Mohsenin/family_form.html'  
    success_url = reverse_lazy('family_list')  # Adjust to your URL's name  


class FamilyDetailView(View):  
    template_name = 'Mohsenin/family_detail.html'  

    def get(self, request, pk):  
        family = get_object_or_404(Family, pk=pk)  
        context = {  
            'family': family  
        }  
        return render(request, self.template_name, context)  


class FamilyUpdateView(UpdateView):  
    model = Family  
    form_class = FamilyForm  # Use a ModelForm for Family  
    template_name = 'Mohsenin/family_form.html'  
    success_url = reverse_lazy('family_list')  # Adjust to your URL's name  


class FamilyDeactivateView(View):  
    template_name = 'Mohsenin/family_confirm_deactivate.html'  

    def get(self, request, pk):  
        family = get_object_or_404(Family, pk=pk)  
        context = {  
            'family': family  
        }  
        return render(request, self.template_name, context)  

    def post(self, request, pk):  
        family = get_object_or_404(Family, pk=pk)  
        family.is_active = False  # Set to inactive  
        family.save()  
        return redirect(reverse_lazy('family_list')) 