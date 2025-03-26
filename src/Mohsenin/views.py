from django.shortcuts import render, get_object_or_404, redirect  
from django.views import View  
from django.views.generic import ListView, CreateView, UpdateView, DeleteView  
from django.urls import reverse_lazy  
from .models import Family, Dist, Person
from .forms import FamilyForm, NewFamilyForm, DistForm, PersonForm

# Create your views here.

def index(request):
    return render(request, 'Mohsenin/index.html')

#-------------- Distribution list views
class DistListView(ListView):
    model = Dist
    template_name = 'Dist/Dist_list.html'
    context_object_name = 'dists'

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        return context


class DistCreateView(CreateView):
    model = Dist
    form_class = DistForm
    template_name = 'Dist/Dist_form.html'
    success_url = reverse_lazy('dist_list')

class DistUpdateView(UpdateView):  
    model = Dist  
    form_class = DistForm  # Use a ModelForm for Family  
    template_name = 'Dist/Dist_form.html'  
    success_url = reverse_lazy('dist_list')

class DistDeleteView(View):  
    def get(self, request, pk):  
        dist = get_object_or_404(Dist, pk=pk)  
        return render(request, 'Dist/dist_confirm_delete.html', {'dist': dist})  
    
    def post(self, request, pk):  
        dist = get_object_or_404(Dist, pk=pk)  
        dist.delete()  
        return redirect(reverse_lazy('dist_list'))

#------------ Family views
class FamilyListView(ListView):  
    model = Family  
    template_name = 'Family/family_list.html'  
    context_object_name = 'families'

    def get_queryset(self):  
        queryset = super().get_queryset()  
        
 

        # Filter by active/inactive  
        active_filter = self.request.GET.get('active_filter')  
        if active_filter == 'active':  
            queryset = queryset.filter(is_active=True)  
        elif active_filter == 'not_active':  
            queryset = queryset.filter(is_active=False)  
        # If the active_filter is not present, we can show not active families by default  
        elif active_filter is None:  
            queryset = queryset.filter(is_active=True) 

        # Check family type based on selected option  
        family_type = self.request.GET.get('family_type')  
        if family_type and family_type != 'all':  
            queryset = queryset.filter(family_type=family_type)  

        return queryset 


class FamilyCreateView(CreateView):  
    model = Family  
    form_class = NewFamilyForm   
    template_name = 'Family/family_form.html'  
    success_url = reverse_lazy('family_list')  


class FamilyDetailView(View):  
    template_name = 'Family/family_detail.html' 

    def get(self, request, pk):  
        family = get_object_or_404(Family, pk=pk)  
        context = {  
            'family': family,  
            'members': family.members.all()  # Access the members directly from the family instance  
        }  
        return render(request, self.template_name, context)
    

class FamilyUpdateView(UpdateView):  
    model = Family  
    form_class = FamilyForm  # Use a ModelForm for Family  
    template_name = 'Family/family_form.html'  
    success_url = reverse_lazy('family_list')  # Adjust to your URL's name  


class FamilyDeactivateView(View):  
    template_name = 'Family/family_confirm_deactivate.html'  

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


#------------ Person views
class PersonListView(View):  
    def get(self, request, family_id):  
        family = get_object_or_404(Family, id=family_id)  
        people = family.people.all()  
        return render(request, 'person/person_list.html', {'family': family, 'people': people})  

class PersonCreateView(View):  
    def get(self, request, family_id):  
        family = get_object_or_404(Family, id=family_id)  
        form = PersonForm(initial={'family': family})  
        return render(request, 'person/person_form.html', {'form': form, 'family': family, 'family_id':family_id})  

    def post(self, request, family_id):  
        family = get_object_or_404(Family, id=family_id)  
        form = PersonForm(request.POST)  
        if form.is_valid():  
            new_person = form.save(commit=False)  
            new_person.family = family  
            new_person.save()  
            return redirect('family_detail', pk=family_id)  
        return render(request, 'person/person_form.html', {'form': form, 'family': family, 'family_id': family_id})  

class PersonUpdateView(View):  
    def get(self, request, family_id, pk):  
        person = get_object_or_404(Person, pk=pk)  
        form = PersonForm(instance=person)  
        return render(request, 'person/person_form.html', {'form': form, 'family_id': family_id})  

    def post(self, request, family_id, pk):  
        person = get_object_or_404(Person, pk=pk)  
        form = PersonForm(request.POST, instance=person)  
        if form.is_valid():  
            form.save()  
            return redirect('family_detail', pk=family_id)  
        return render(request, 'person/person_form.html', {'form': form, 'family_id': family_id})

def set_guardian(request, family_id, pk):
    person = get_object_or_404(Person, pk=pk)
    family = get_object_or_404(Family, id=family_id)
    family.guardian = person
    family.save();
    return redirect('family_detail', pk=family_id)

 


#-------------- Observation views
class ObservationListView(View):  
    def get(self, request, family_id):  
        family = get_object_or_404(Family, id=family_id)  
        observations = family.observation_set.all()  
        return render(request, 'observations/observation_list.html', {'family': family, 'observations': observations})  
