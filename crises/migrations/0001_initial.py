<<<<<<< HEAD
# Generated by Django 3.2.4 on 2021-06-17 20:14
=======
<<<<<<< HEAD
# Generated by Django 3.2.4 on 2021-06-16 16:46
=======
# Generated by Django 3.2.4 on 2021-06-17 14:41
>>>>>>> 7b49f76b63b6a7c46f5a164371296883e3c6c658
>>>>>>> development

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crisis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disaster_type', models.CharField(choices=[('Tsunami', 'Tsunami'), ('Hurricane', 'Hurricaine'), ('Flood', 'Flood'), ('Earthquake', 'Earthquake'), ('War', 'War'), ('Pandemic', 'Pandemic'), ('Wildfire', 'Wildfire')], max_length=20)),
                ('is_solved', models.BooleanField()),
<<<<<<< HEAD
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=11)),
                ('place_name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=70)),
                ('disaster_description', models.TextField(max_length=1000)),
=======
<<<<<<< HEAD
=======
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('place_name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=70)),
                ('disaster_description', models.TextField(max_length=1000)),
>>>>>>> 7b49f76b63b6a7c46f5a164371296883e3c6c658
>>>>>>> development
            ],
        ),
        migrations.CreateModel(
            name='NGOResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_type', models.CharField(choices=[('Human', 'Human'), ('Material', 'Material')], max_length=20)),
                ('resource_name', models.CharField(choices=[('Doctor', 'Doctor'), ('Nurse', 'Nurse'), ('Helper', 'Helper'), ('Teacher', 'Teacher'), ('Rescuer', 'Rescuer'), ('Medical', 'Medical'), ('Nutrition', 'Nutrition'), ('Clothes', 'Clothes'), ('Shelter', 'Shelter'), ('Transport', 'Transport')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('crisis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='crises.crisis')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='crises.resource')),
            ],
        ),
    ]
