# models.py in EmployeeApp

from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
import os


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLES_CHOICES = (
        ('hr_manager', _('HR Manager')),
        ('manager', _('Manager')),
        ('employee', _('Employee')),
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    roles = models.CharField(max_length=255, choices=ROLES_CHOICES, default='employee', verbose_name=_('Roles'))
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    is_subscribed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    preferred_language = models.CharField(max_length=10, default='fr')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

    # Set unique related_name for groups and user_permissions
    CustomUser._meta.get_field('groups').related_name = 'custom_user_groups'
    CustomUser._meta.get_field('user_permissions').related_name = 'custom_user_permissions'










######################################################################################################################################""









from django.conf import settings


class Traceability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=255)
    action_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action_type} by {self.user} at {self.action_date}"
from django.db import models
from django.contrib.auth.models import User

class Onboarding(models.Model):
    nomCycle = models.CharField(max_length=255)

    def __str__(self):
        return self.nomCycle

class EtapeOnboarding(models.Model):
    numeroEtape = models.IntegerField()
    description = models.TextField()
    onboarding = models.ForeignKey(Onboarding, on_delete=models.CASCADE, related_name='etapes', null=True, blank=True)

    def __str__(self):
        return f"Step {self.numeroEtape}: {self.description}"

class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ('email', 'Email Task'),
        ('calendar', 'Calendar Task'),
    ]
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES)
    description = models.TextField()
    etape = models.ForeignKey(EtapeOnboarding, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField(null=True, blank=True)
    first_alert_date = models.DateField(null=True, blank=True)
    second_alert_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.description

class Notification(models.Model):
    task = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}"

class TeamManager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team = models.ForeignKey(Onboarding, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return self.user.username

class OnboardingProgress(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='onboarding_progress')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.task.description}"



class Department(models.Model):
    depName = models.CharField(max_length=255)
    depLevel = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8)
        ]
    )
    employees = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employee_departments', default=None, null=True)
    numOfEmployees = models.IntegerField()

    def __str__(self):
        return self.depName


class Equipe(models.Model):
    name = models.CharField(max_length=100, help_text="Nom de l'équipe")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='equipes', help_text="Département auquel l'équipe est associée", null=True, blank=True)
    equipe_leader = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, related_name='equipes_led', help_text="Chef d'équipe", null=True, blank=True)
    equipe_leader_backup = models.ForeignKey('Employee', on_delete=models.DO_NOTHING, related_name='equipes_backup', help_text="Chef d'équipe suppléant", null=True, blank=True)

    def __str__(self):
        return self.name



class Competence(models.Model):
    tache = models.ForeignKey('Tache', on_delete=models.DO_NOTHING, related_name='competences', help_text="Tâche")
    diplome = models.CharField(max_length=100, default="", help_text="Diplôme validant la compétence")
    autorisation = models.BooleanField(blank=True, null=True, help_text="Autorisation requise")
    certificat_formation = models.BooleanField(blank=True, null=True, help_text="Certificat de formation")
    nombre_annees_experience = models.IntegerField(default=0, help_text="Nombre d'années d'expérience")

    def __str__(self):
        return f"{self.tache} - {self.diplome}"


def validate_pdf(file):
    ext = os.path.splitext(file.name)[1]  # Extract the file extension
    if ext.lower() != '.pdf':
        raise ValidationError('Only PDF files are allowed.')

class Employee(models.Model):
    employeeID = models.IntegerField()
    firstName = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=255)
    department = models.ForeignKey('EmployeeApp.Department', on_delete=models.CASCADE, related_name='employee_departments')
    employmentType = models.CharField(max_length=255)
    email = models.EmailField()
    startDate = models.DateField()
    departureDate = models.DateField(null=True, blank=True)  # Allow null and blank values
    sanctions = models.TextField()
    handicap = models.CharField(max_length=255, null=True, blank=True)
    salary = models.FloatField()
    retirementDate = models.DateField(null=True, blank=True)
    employeeCarreerHistory = models.TextField()
    onboarding = models.ForeignKey('Onboarding', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    competences = models.ManyToManyField('Competence', through='EmployeeCompetence', related_name='employees')
    matricule = models.CharField(max_length=8, unique=True, default=None, null=False, validators=[RegexValidator(regex='^\d{8}$', message='Le matricule doit contenir exactement 8 chiffres.')])

    emplacement = models.CharField(max_length=255, default=None)

    photo = models.ImageField(blank=True, upload_to="employees/photos/", verbose_name="Photo")

    performance_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Performance Rate (%)")

    cv = models.FileField(upload_to='employees/cvs/', validators=[validate_pdf], null=True, blank=True)

    parentId = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', db_column='parentId')
    contract_type = models.CharField(max_length=100, blank=True, null=True)
    def calculate_performance_rate(self):

        sanctions_factor = 1 - (len(self.sanctions) / 100)  # na9as fih % aux sanctions
        salary_factor = self.salary / 5000
        availability_factor = 1
        leave_factor = 1 - (0.02 * len(self.leave_set.all()))

        performance_rate = (
                                   (sanctions_factor * 0.3) +
                                   (salary_factor * 0.4) +
                                   (availability_factor * 0.2) +
                                   (leave_factor * 0.1)
                           ) * 100
        return min(max(performance_rate, 0), 100)


    def save(self, *args, **kwargs):
        action_type = "Saisie de position administrative"
        action_details = f"Position administrative ajoutée pour {self.firstName} {self.lastName}"


        Traceability.objects.create(action_type=action_type, details=action_details)

        super(Employee, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.firstName} {self.lastName}"




class EmployeeCompetence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_competences')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name='competence_employees')

    def __str__(self):
        return f"{self.employee} - {self.competence}"


class Poste(models.Model):
    nom = models.CharField(max_length=100, default="", help_text="Nom du poste")
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='postes', help_text="Employé")
    evaluation = models.IntegerField(default=0, help_text="Evaluation de l'atteinte de l'objectif(0..100)")
    indice_consommation = models.DecimalField(default=0, decimal_places=2, max_digits=5, help_text="Indice de consommation du budget(0..100)")
    budget = models.DecimalField(default=0, decimal_places=2, max_digits=10, help_text="Budget du poste")
    conges_supp = models.DecimalField(default=0, decimal_places=2, max_digits=5, help_text="Congés supplémentaires")
    objects = models.Manager()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_fermeture = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nom

from django.db import models

class Tache(models.Model):
    poste = models.ForeignKey('Poste', on_delete=models.DO_NOTHING, related_name='taches', help_text="Poste")
    titre = models.CharField(max_length=100, default="", help_text="Titre de la tâche")
    description = models.TextField(blank=True, help_text="Description de la tâche")
    budget = models.DecimalField(default=0, decimal_places=2, max_digits=10, help_text="Budget de la tâche")
    budget_min = models.DecimalField(default=0, decimal_places=2, max_digits=10, help_text="Budget minimum de la tâche")
    date_debut = models.DateField(help_text="Date de début")
    date_fin = models.DateField(help_text="Date de fin", null=True, blank=True)
    presence = models.BooleanField(blank=True, null=True, help_text="Présence sur site")

    def __str__(self):
        return self.titre



class Affectation(models.Model): #des employees a prpos les postes
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)
    ratio = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('employee', 'poste')



class EmploymentHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employer = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    responsibilities = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.employer} - {self.position}"

class ContractType(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the contract type")

    def __str__(self):
        return self.name

class Contract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts')
    contract_type = models.ForeignKey(ContractType, on_delete=models.CASCADE, related_name='contracts')
    start_date = models.DateField()
    end_date = models.DateField()
    duration_regulation = models.IntegerField(help_text="Regulatory duration for the contract type (in months)")

    def __str__(self):
        return f"{self.employee} - {self.contract_type} Contract: {self.start_date} to {self.end_date}"


class Leave(models.Model):   #congé
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_set')
    start_date = models.DateField()
    end_date = models.DateField()
    departure_reason = models.CharField(max_length=100, default=None,help_text="Name of the departure reason")

    def __str__(self):
        return f"{self.employee} - Leave: {self.start_date} to {self.end_date}"

