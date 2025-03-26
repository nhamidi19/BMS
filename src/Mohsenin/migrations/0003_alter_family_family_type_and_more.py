# Generated by Django 5.1.7 on 2025-03-26 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mohsenin', '0002_package_dist_note_inmaterelease_medicalaid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='family_type',
            field=models.IntegerField(choices=[(1, 'یتیم'), (2, 'زندانی'), (3, 'مطلقه'), (4, 'رها شده'), (5, 'بیمار'), (6, 'فقیر')], default=1, verbose_name='نوع نیازمندی'),
        ),
        migrations.AlterField(
            model_name='medicalaid',
            name='estimated_cost',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
