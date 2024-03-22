# models.py in EmployeeApp

from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models


class Onboarding(models.Model):
    nomCycle = models.CharField(max_length=255)

    def __str__(self):
        return self.nomCycle

class EtapeOnboarding(models.Model):
    numeroEtape = models.IntegerField()
    description = models.TextField()
    onboarding = models.ForeignKey('Onboarding', on_delete=models.CASCADE, related_name='etapes', null=True, blank=True)

class Department(models.Model):
    depName = models.CharField(max_length=255)
    depLevel = models.IntegerField()
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

    competences = models.ManyToManyField(Competence, through='EmployeeCompetence', related_name='employees')

    matricule = models.CharField(max_length=8, unique=True, default='',validators=[RegexValidator(regex='^\d{8}$', message='Le matricule doit contenir exactement 8 chiffres.')])


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

    def __str__(self):
        return self.nom

class Tache(models.Model):
    poste = models.ForeignKey('Poste', on_delete=models.DO_NOTHING, related_name='taches', help_text="Poste")
    titre = models.CharField(max_length=100, default="", help_text="Titre de la tâche")
    description = models.TextField(blank=True, help_text="Description de la tâche")
    budget = models.DecimalField(default=0, decimal_places=2, max_digits=10, help_text="Budget de la tâche")
    budget_min = models.DecimalField(default=0, decimal_places=2, max_digits=10, help_text="Budget minimum de la tâche")
    date_debut = models.DateField(help_text="Date de début")
    date_fin = models.DateField(help_text="Date de fin",null=True,blank=True)
    presence = models.BooleanField(blank=True, null=True, help_text="Présence sur site")


class Affectation(models.Model):
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








