from django.shortcuts import render, get_object_or_404, redirect  
from django.views import View  
from django.views.generic import ListView, CreateView, UpdateView, DeleteView , DetailView
from django.urls import reverse_lazy
import jdatetime
from jdatetime import JalaliToGregorian
from .xml_maker import convert_xml
from .models import *
from .forms import *

# Create your views here.

def conver_solar_date(date):
    return jdatetime.datetime.fromgregorian(datetime=date).strftime("%Y/%m/%d")


def index(request):
    return render(request, 'Mohsenin/index.html')

  # You need to create this form 
  # 
#------------ Distribution List
class DistListView(ListView):
    model = Dist
    template_name = 'Dist/Dist_list.html'
    context_object_name = "dists"



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

class DistDeleteView(DeleteView):  
    model = Dist
    template_name = "Dists/dists_confirm_delete.html"
    success_url = reverse_lazy("dist_list")
    def get(self, request, pk):  
        dist = get_object_or_404(Dist, pk=pk)  
        return render(request, 'Dist/dist_confirm_delete.html', {'dist': dist})  



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


def family_list(request):
    return convert_xml(Family)


class FamilyCreateView(CreateView):  
    model = Family  
    form_class = NewFamilyForm  
    template_name = 'Family/family_form.html'  
    success_url = reverse_lazy('family_list') 


class FamilyDetailView(CreateView):  
    # template_name = 'Family/family_detail.html'
    # model = Person
    # form_class = NewPersonForm
    # success_url = reverse_lazy("person_list")

    # def get(self, request, pk):  
    #     family = get_object_or_404(Family, pk=pk)  
    #     context = {  
    #         'family': family,
    #     } 
    #     return render(request, self.template_name, context)  
    # def post(self, request, pk):  
    #     family = get_object_or_404(Family, pk=pk)  
    #     family.family = family
    #     context = {  
    #         'family': family,
    #     }  
    #     return render(request, self.template_name, context) 
    template_name = 'Family/family_detail.html'
    model = Person
    form_class = NewPersonForm
    success_url = reverse_lazy("person_list")

    def get(self, request, pk):
        family = get_object_or_404(Family, pk=pk)
        person = Person.objects.all()
        context = {
            'persons':person,
            'family': family,
            'form': NewPersonForm(),  # فرم اولیه برای نمایش
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        family = get_object_or_404(Family, pk=pk)
        form = NewPersonForm(request.POST)  # Filling the form with submitted data
        if form.is_valid():
            person = form.save(commit=False)
            
            # Converting Jalali (Shamsi) date to Gregorian date
            jalali_date = form.cleaned_data['birth_date']  # Replace with your field name
            gregorian_date = jdatetime.date(
                jalali_date.year, jalali_date.month, jalali_date.day
            ).togregorian()  # Use the `togregorian` method
            
            person.birth_date = gregorian_date  # Store the Gregorian date in the database
            person.family = family  # Associate the person with the family
            person.save()
            
            return redirect("person_list" ,family_id=pk)  # Redirect to success_url
        else:
            context = {
                'family': family,
                'form': form,  # Display form with errors
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

#----------------persons View

class PersonListView(ListView):  
    model = Person
    template_name = 'Person/person_list.html'  
    context_object_name = 'persons'
    def get(self, request, family_id):
        members = Person.objects.filter(family_id=family_id)
        family = Family.objects.get(id=family_id)
        for member in members:
            member.birth_date = conver_solar_date(member.birth_date)
        context = {
            "persons" : members,
            "family": family,
        }
        return render(request , self.template_name, context)
    
def person_list(requrst):
    return convert_xml(Person)



class PersonCreateView(CreateView):  
    model = Person  
    form_class = NewPersonForm  # Use a ModelForm for Family  
    template_name = 'Person/person_form.html'  
    success_url = reverse_lazy('person_list')  # Adjust to your URL's name 

    def post(self, request, family_id):
        family = Family.objects.get(id=family_id)
        form = NewPersonForm(request.POST)
        if form.is_valid():
            family_form = form.save(commit=False)
            family_form.family = family
            family_form.save()
            return redirect("person_list", family_id=family_id)
        else:
            # در صورت نامعتبر بودن فرم، فرم را دوباره با خطاها رندر کنید
            return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        jalali_date = form.cleaned_data['birth_date']  
        gregorian_date = jdatetime.date(
            jalali_date.year, jalali_date.month, jalali_date.day
        ).togregorian()  

        form.instance.birth_date = gregorian_date  
        self.object = form.save()  # Set self.object
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the Family object by ID, ensure the ID is properly provided
        family_id = self.kwargs.get('family_id')  # Assuming you're passing 'family_id' in the URL
        context['family'] = get_object_or_404(Family, id=family_id)
        return context




class PersonDetailView(View):  
    template_name = 'Person/person_detail.html'

    def get(self, request, pk):  
        persons = get_object_or_404(Person, pk=pk)  
        persons.birth_date = conver_solar_date(persons.birth_date)

        context = {  
            'person': persons,
        } 
        return render(request, self.template_name, context)  


class PersonUpdateView(UpdateView):  
    model = Person  
    form_class = NewPersonForm 
    context_object_name = "person"
    template_name = 'Person/person_form.html'
    success_url = reverse_lazy('person_list')  

    def get_initial(self):
            initial = super().get_initial()
            instance = self.get_object()
            if instance.birth_date:  
                gregorian_date = instance.birth_date
                jalali_date = jdatetime.date.fromgregorian(
                    year=gregorian_date.year,
                    month=gregorian_date.month,
                    day=gregorian_date.day
                )
                initial['birth_date'] = jalali_date  # تاریخ جلالی برای نمایش در فرم
            return initial

    def form_valid(self, form):
        jalali_date = form.cleaned_data['birth_date']  # تاریخ واردشده توسط کاربر (جلالی)
        gregorian_date = jdatetime.date(
            jalali_date.year, jalali_date.month, jalali_date.day
        ).togregorian()  # تبدیل به میلادی

        form.instance.birth_date = gregorian_date  # ذخیره تاریخ میلادی در مدل
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the Family object by ID, ensure the ID is properly provided
        family_id = self.kwargs.get('family_id')  # Assuming you're passing 'family_id' in the URL
        context['family'] = get_object_or_404(Family, id=family_id)
        return context
    

    def get_success_url(self):
        family_id = self.kwargs.get('family_id')  # گرفتن family_id از URL
        return reverse_lazy('person_list', kwargs={'family_id': family_id})  # ساخت success_url با family_id



class PersonDeactivateView(View):  
    template_name = 'Person/person_confirm_deactivate.html'  

    def get(self, request, family_id, pk):  
        family = Family.objects.get(id=family_id)
        person = Person.objects.get(id=pk, family=family)
        context = {  
            'person': person,
            "family": family,
        }  
        return render(request, self.template_name, context)  

    def post(self, request, family_id, pk): 
        family = Family.objects.get(id=family_id)
        person = Person.objects.get(id=pk, family=family)
        person.is_guardian = False  
        person.save()
        return redirect(reverse_lazy('person_list'))





#-------------- Observation views
class ObservationListView(View):  
    def get(self, request, family_id):  
        family = get_object_or_404(Family, id=family_id)  
        observations = family.observation_set.all()
        for observation in observations:
            observation.observation_date = conver_solar_date(observation.observation_date)
        
        return render(request, 'observations/observation_list.html', {'family': family, 'observations': observations}) 

def observation_list(request):
    return convert_xml(Observation) 


class ObservationCreateView(View):
    def get(self, request, family_id):
        family = get_object_or_404(Family, id=family_id)
        form = ObservationForm()  

        context = {
            'family': family,
            'form': form,  
        }
        return render(request, "Observations/observation_form.html", context)
    
    def post(self, request, family_id):
        family = get_object_or_404(Family, id=family_id)
        form = ObservationForm(request.POST) 
        if form.is_valid():
            observation = form.save(commit=False)
            
            # Convert Jalali date to Gregorian
            jalali_date = form.cleaned_data.get("observation_date")
            if jalali_date:
                gregorian_date = jdatetime.date(
                    jalali_date.year, jalali_date.month, jalali_date.day
                ).togregorian()
                observation.observation_date = gregorian_date
            
            observation.family = family
            observation.save()
            return redirect("observation_list", family_id=family_id)  
        else:
            context = {"family": family, "form": form}
            return render(request, "Observations/observation_form.html", context)


class ObservationsDetailsView(View):
    template_name = "Observations/observation_detail.html"
    def get(self, request, family_id , observation_id):
        family = get_object_or_404(Family, id=family_id)
        observation = Observation.objects.get(id=observation_id, family=family)
        observation.observation_date = conver_solar_date(observation.observation_date)
        context = {
            "observation": observation,
            "family": family
        }
        return render(request, self.template_name, context)



class ObservationsUpdateView(UpdateView):
    template_name = "Observations/observation_form.html"
    model = Observation
    form_class = ObservationForm
    pk_url_kwargs = "observation_id"

    def get(self, request, family_id, observation_id):
        form = ObservationForm()
        family = Family.objects.get(id=family_id)
        observation = Observation.objects.get(id=observation_id)
        context = {
            "family": family,
            "observation": observation,
            "form": form,
        }
        return render(request, self.template_name, context)
        


    
    def get_object(self, queryset=None):
        return get_object_or_404(Observation, id=self.kwargs.get("observation_id"))

    def get_initial(self):
        initial = super().get_initial()
        observation = self.get_object()
        if observation.observation_date:
            gregorian_date = observation.observation_date
            jalali_date = jdatetime.date.fromgregorian(
                year=gregorian_date.year,
                month=gregorian_date.month,
                day=gregorian_date.day
            )
            initial['observation_date'] = jalali_date 
        return initial

    def get_success_url(self):
        return reverse_lazy("observation_list", kwargs={"family_id": self.object.family.id})




class ObservationsDeleteView(DeleteView):
    template_name = "Observations/observation_confirm_delete.html"
    model = Observation
    context_object_name = "observation"

    def get_object(self, quersyset=None):
        return get_object_or_404(Observation, id=self.kwargs.get("observation_id"))

    def get_success_url(self):
        return reverse_lazy("observation_list", kwargs={"family_id":self.object.family.id})



#-------------- Packages views
class PackageListView(ListView):
    template_name = "Package/package_list.html"
    model = Package
    context_object_name = "packages"


def package_list(request):
    return convert_xml(Package)


class PackageCreateView(CreateView):
    template_name = "Package/packages_form.html"
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy("packages_list")


class PackageUpdateView(UpdateView):
    model = Package
    form_class = PackageForm
    success_url = reverse_lazy('packages_list')
    template_name = "Package/packages_form.html"


class PackageDeleteView(DeleteView):
    model = Package
    success_url = reverse_lazy("packages_list")
    template_name = "Package/packages_confirm_delete.html"


class PackageDetailView(DetailView):
    model = Package
    template_name = "Package/package_detail.html"
    context_object_name = "package"




#-------------- PackageDistribution views
class PackageDistributionListView(ListView):
    template_name = "PackageDistribution/packagedistribution_list.html"
    model = PackageDistribution
    context_object_name = "packagedistributions"

    def get_queryset(self):
        queryset = super().get_queryset()  
        for packagedistribution in queryset:
            packagedistribution.distribution_date = conver_solar_date(packagedistribution.distribution_date)
        return queryset
    

def packageDistribtion_list(request):
    return convert_xml(PackageDistribution)
    
class PackageDistributionCreate(CreateView):
    template_name = "PackageDistribution/packagedistribution_form.html"
    model = PackageDistribution
    form_class = PackageDistributionForm
    success_url = reverse_lazy("packageshare_list")


    def form_valid(self, form):
        jalali_date = form.cleaned_data['distribution_date']  
        gregorian_date = jdatetime.date(
            jalali_date.year, jalali_date.month, jalali_date.day
        ).togregorian()  

        form.instance.distribution_date = gregorian_date  
        return super().form_valid(form)
    

class PackageDistributionUpdate(UpdateView):
    model = PackageDistribution
    form_class = PackageDistributionForm
    context_object_name = "packagedistribution"
    template_name = 'PackageDistribution/packagedistribution_form.html'
    success_url = reverse_lazy('packageshare_list')

    def get_initial(self):
        initial = super().get_initial()
        instance = self.get_object()
        if instance.distribution_date:
            gregorian_date = instance.distribution_date
            jalali_date = jdatetime.date.fromgregorian(
                year=gregorian_date.year,
                month=gregorian_date.month,
                day=gregorian_date.day
            )
            initial['distribution_date'] = jalali_date
        return initial

    def form_valid(self, form):
        # تبدیل تاریخ شمسی به میلادی
        jalali_date = form.cleaned_data['distribution_date']
        if jalali_date:
            gregorian_date = jdatetime.date(
                jalali_date.year, jalali_date.month, jalali_date.day
            ).togregorian()
            form.instance.distribution_date = gregorian_date
        return super().form_valid(form)
    
class PackageDistributionDetail(DetailView):
    model = PackageDistribution
    template_name = 'PackageDistribution/packagedistribution_detail.html'
    context_object_name = 'packagedistribution'


class PackageDistributionDeactive(View):
    template_name = 'PackageDistribution/packagedistribution_confirm_deactive.html'  

    def get(self, request, pk):  
        packagedistribution = get_object_or_404(PackageDistribution, pk=pk)
        context = {  
            'package_share': packagedistribution
        }  
        return render(request, self.template_name, context)  

    def post(self, request, pk):  
        packagedistribution = get_object_or_404(PackageDistribution, pk=pk) 
        packagedistribution.is_active = False  
        packagedistribution.save()
        return redirect(reverse_lazy('packageshare_list'))
    

class MedicalAidListView(ListView):
    template_name = "Medicalaid/medicalaid_list.html"
    model = MedicalAid
    context_object_name = "medicalaids"

def medicalaidlist(request):
    return convert_xml(MedicalAid)

class MedicalAidCreateView(CreateView):
    template_name = "Medicalaid/medicalaid_form.html"
    model = MedicalAid
    form_class = MedicalAidForm
    context_object_name = "inmaterelease"
    success_url = reverse_lazy("medicalaid_list")

class MedicalAidUpdateView(UpdateView):
    template_name = "Medicalaid/medicalaid_form.html"
    model = MedicalAid
    form_class = MedicalAidForm
    # success_url = reverse_lazy("medicalaid_detail")

    def get_success_url(self):
        return reverse_lazy("medicalaid_detail", kwargs={"pk":self.object.id})

class MedicalAidDetailView(DetailView):
    template_name = "Medicalaid/medicalaid_detail.html"
    model = MedicalAid
    context_object_name = "medicalaid"

class MedicalAidDeactiveView(View):
    template_name = "Medicalaid/medicalaid_confirm_deactive.html"

    def get(self, request, pk):  
        medicalaid = get_object_or_404(MedicalAid, pk=pk)  
        context = {  
            'medicalaid': medicalaid  
        }  
        return render(request, self.template_name, context)  

    def post(self, request, pk):  
        medicalaid = get_object_or_404(MedicalAid, pk=pk)  
        medicalaid.is_active = False  # Set to inactive  
        medicalaid.save()
        return redirect(reverse_lazy('medicalaid_list'))


#-------------- PackageDistribution views
class InmateReleaseListView(ListView):
    template_name = "InmateRelease/inmaterelease_list.html"
    model = InmateRelease
    context_object_name = "inmatereleases"

    def get(self, request):
        objects = InmateRelease.objects.all()
        for object_n in objects:
            object_n.release_date = conver_solar_date(object_n.release_date)
        context = {
            "inmatereleases": objects
        }
        return render(request, self.template_name, context)
    

def inmaterelease_list(request):
    return convert_xml(InmateRelease)



class InmateReleaseCreateView(CreateView):
    template_name = "InmateRelease/inmaterelease_form.html"
    model = InmateRelease
    form_class = InmateReleaseForm
    success_url = reverse_lazy("inmaterelease_list")

    def form_valid(self, form):
        jalali_date = form.cleaned_data['release_date']  # فرض بر این است که کاربر تاریخ جلالی وارد کرده است
        gregorian_date = jdatetime.date(
            jalali_date.year, jalali_date.month, jalali_date.day
        ).togregorian()  # تبدیل تاریخ جلالی به میلادی
        
        form.instance.release_date = gregorian_date  # مقدار میلادی در مدل ثبت می‌شود
        return super().form_valid(form)


class InmateReleaseUpdateView(UpdateView):
    template_name = "InmateRelease/inmaterelease_form.html"
    model = InmateRelease
    form_class = InmateReleaseForm
    pk_url_kwarg = "pk_object"
    context_object_name = "inmaterelease"

    def get_initial(self):
        initial = super().get_initial()
        instance = self.get_object()
        if instance.release_date:  
            gregorian_date = instance.release_date
            jalali_date = jdatetime.date.fromgregorian(
                year=gregorian_date.year,
                month=gregorian_date.month,
                day=gregorian_date.day
            )
            initial['release_date'] = jalali_date  # تاریخ جلالی برای نمایش در فرم
        return initial

    def form_valid(self, form):
        jalali_date = form.cleaned_data['release_date']  # تاریخ واردشده توسط کاربر (جلالی)
        gregorian_date = jdatetime.date(
            jalali_date.year, jalali_date.month, jalali_date.day
        ).togregorian()  # تبدیل به میلادی

        form.instance.release_date = gregorian_date  # ذخیره تاریخ میلادی در مدل
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("inmaterelease_detail", kwargs={"pk_object": self.object.pk})

    
class InmateReleaseDetail(DetailView):
    template_name = "InmateRelease/inmaterelease_detail.html"
    model = InmateRelease
    context_object_name = "inmaterelease"
    pk_url_kwarg = "pk_object"

    def get(self, request, pk_object):
        inmate = InmateRelease.objects.get(id=pk_object)
        inmate.release_date = conver_solar_date(inmate.release_date)
        context = {
            "inmaterelease": inmate
        }
        return render(request, self.template_name, context)
    
