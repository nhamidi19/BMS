from django.db import models

from .choices import NEED_LEVEL_CHOICE, FAMILY_TYPE_CHOICES

class Dist(models.Model): #Distribution List
    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(default="")

    def familycount(self):
        return self.family_set.count()

    def __str__(self):
        return self.name

# Create your models here.
class Family(models.Model):
    doc_code = models.IntegerField('شماره پرونده')
    need_level = models.IntegerField('سطح نیاز', default=1, choices=NEED_LEVEL_CHOICE)
    family_type = models.IntegerField('نوع نیازمندی', default=1, choices=FAMILY_TYPE_CHOICES)
    guardian = models.ForeignKey('Person', verbose_name='سرپرست خانوار', on_delete=models.SET_NULL, related_name='guardianship', null=True)
    address = models.CharField('آدرس',max_length=255)
    contact_number = models.CharField('شماره تماس',max_length=15, blank=True, null=True)
    postal_code = models.CharField('کدپستی',max_length=10, blank=True, null= True)
    distlist = models.ForeignKey(Dist, verbose_name='لیست توزیع',on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField('تحت پوشش',default=True)  # To track if the family is currently receiving support


class Person(models.Model):
    family = models.ForeignKey(Family, related_name='members', on_delete=models.CASCADE)
    first_name = models.CharField('نام',max_length=50)
    last_name = models.CharField('نام خانوادگی',max_length=50)
    father_name = models.CharField('', max_length=50)
    national_id = models.CharField('شماره ملی', max_length=10)
    birth_date = models.DateField('تاریخ تولد') #TODO: USE django-jalali
    is_orphan = models.BooleanField('یتیم')
    is_guardian = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
class Observation(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=100)
    observation_date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"Observation for {self.family} by {self.agent_name} on {self.observation_date}"

class Package(models.Model):
    name = models.CharField(max_length=100)
    max_members = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class PackageDistribution(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    members = models.ManyToManyField(Person, related_name='packages')
    distribution_date = models.DateField()
    is_active = models.BooleanField(default=True)  # To track if the package is still valid for the family

    def __str__(self):
        return f"{self.package} distributed to {self.family} on {self.distribution_date}"

class MedicalAid(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    medical_needs = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Medical Aid for {self.family}"

    def clean(self):
        # Ensure that sick families have medical needs specified
        # code 5 means Sick Family
        if self.family.family_type != 5:
            raise ValidationError("Medical aid can only be assigned to sick families.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class InmateRelease(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    release_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inmate release for {self.family} on {self.release_date}"