# Generated by Django 5.0.2 on 2024-03-25 14:11

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diplome', models.CharField(default='', help_text='Diplôme validant la compétence', max_length=100)),
                ('autorisation', models.BooleanField(blank=True, help_text='Autorisation requise', null=True)),
                ('certificat_formation', models.BooleanField(blank=True, help_text='Certificat de formation', null=True)),
                ('nombre_annees_experience', models.IntegerField(default=0, help_text="Nombre d'années d'expérience")),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depName', models.CharField(max_length=255)),
                ('depLevel', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('numOfEmployees', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Onboarding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomCycle', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeID', models.IntegerField()),
                ('firstName', models.CharField(blank=True, max_length=255, null=True)),
                ('lastName', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('position', models.CharField(max_length=255)),
                ('employmentType', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('startDate', models.DateField()),
                ('departureDate', models.DateField(blank=True, null=True)),
                ('sanctions', models.TextField()),
                ('handicap', models.CharField(blank=True, max_length=255, null=True)),
                ('salary', models.FloatField()),
                ('retirementDate', models.DateField(blank=True, null=True)),
                ('employeeCarreerHistory', models.TextField()),
                ('matricule', models.CharField(default=None, max_length=8, unique=True, validators=[django.core.validators.RegexValidator(message='Le matricule doit contenir exactement 8 chiffres.', regex='^\\d{8}$')])),
                ('level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(8)])),
                ('emplacement', models.CharField(default=None, max_length=255)),
                ('performance_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Performance Rate (%)')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_departments', to='EmployeeApp.department')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='employees',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_departments', to='EmployeeApp.employee'),
        ),
        migrations.CreateModel(
            name='EmployeeCompetence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competence_employees', to='EmployeeApp.competence')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_competences', to='EmployeeApp.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='competences',
            field=models.ManyToManyField(related_name='employees', through='EmployeeApp.EmployeeCompetence', to='EmployeeApp.competence'),
        ),
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('responsibilities', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Nom de l'équipe", max_length=100)),
                ('department', models.ForeignKey(blank=True, help_text="Département auquel l'équipe est associée", null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipes', to='EmployeeApp.department')),
                ('equipe_leader', models.ForeignKey(blank=True, help_text="Chef d'équipe", null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipes_led', to='EmployeeApp.employee')),
                ('equipe_leader_backup', models.ForeignKey(blank=True, help_text="Chef d'équipe suppléant", null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipes_backup', to='EmployeeApp.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_set', to='EmployeeApp.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EtapeOnboarding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroEtape', models.IntegerField()),
                ('description', models.TextField()),
                ('onboarding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='etapes', to='EmployeeApp.onboarding')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='onboarding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='EmployeeApp.onboarding'),
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default='', help_text='Nom du poste', max_length=100)),
                ('evaluation', models.IntegerField(default=0, help_text="Evaluation de l'atteinte de l'objectif(0..100)")),
                ('indice_consommation', models.DecimalField(decimal_places=2, default=0, help_text='Indice de consommation du budget(0..100)', max_digits=5)),
                ('budget', models.DecimalField(decimal_places=2, default=0, help_text='Budget du poste', max_digits=10)),
                ('conges_supp', models.DecimalField(decimal_places=2, default=0, help_text='Congés supplémentaires', max_digits=5)),
                ('employee', models.ForeignKey(help_text='Employé', on_delete=django.db.models.deletion.CASCADE, related_name='postes', to='EmployeeApp.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Tache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(default='', help_text='Titre de la tâche', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Description de la tâche')),
                ('budget', models.DecimalField(decimal_places=2, default=0, help_text='Budget de la tâche', max_digits=10)),
                ('budget_min', models.DecimalField(decimal_places=2, default=0, help_text='Budget minimum de la tâche', max_digits=10)),
                ('date_debut', models.DateField(help_text='Date de début')),
                ('date_fin', models.DateField(blank=True, help_text='Date de fin', null=True)),
                ('presence', models.BooleanField(blank=True, help_text='Présence sur site', null=True)),
                ('poste', models.ForeignKey(help_text='Poste', on_delete=django.db.models.deletion.DO_NOTHING, related_name='taches', to='EmployeeApp.poste')),
            ],
        ),
        migrations.AddField(
            model_name='competence',
            name='tache',
            field=models.ForeignKey(help_text='Tâche', on_delete=django.db.models.deletion.DO_NOTHING, related_name='competences', to='EmployeeApp.tache'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('can_edit_posts', models.BooleanField(default=False)),
                ('can_delete_comments', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('is_subscribed', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('preferred_language', models.CharField(default='fr', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Traceability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(max_length=255)),
                ('action_date', models.DateTimeField(auto_now_add=True)),
                ('details', models.TextField(blank=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Affectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.employee')),
                ('poste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.poste')),
            ],
            options={
                'unique_together': {('employee', 'poste')},
            },
        ),
    ]