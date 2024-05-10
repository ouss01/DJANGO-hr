from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseNotFound
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.utils import json

from .models import (
    Department, Employee, Poste, Tache,
    Competence, Onboarding, EtapeOnboarding,
    Equipe, Affectation, EmploymentHistory
)
from .forms import PosteForm, UserRegistrationForm
from .serializers import (
    DepartmentSerializer, EmployeeSerializer, PosteSerializer,
    TacheSerializer, CompetenceSerializer, EquipeSerializer,
    EtapeOnboardingSerializer, OnboardingSerializer,
    EmployeeCompetenceSerializer, AffectationSerializer,
    EmploymentHistorySerializer
)


# Department Views
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def department_api(request, id=0):
    try:
        if request.method == 'GET':
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            department_data = request.data
            serializer = DepartmentSerializer(data=department_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Department added successfully.", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            department_data = request.data
            department = get_object_or_404(Department, id=id)
            serializer = DepartmentSerializer(department, data=department_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Department updated successfully.", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            department = get_object_or_404(Department, id=id)
            department.delete()
            return Response("Department deleted successfully.", status=status.HTTP_204_NO_CONTENT)

    except Department.DoesNotExist:
        return HttpResponseNotFound("Department not found")


# Employee Views
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def employee_api(request, id=0):
    try:
        if request.method == 'GET':
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            employee_data = request.data
            serializer = EmployeeSerializer(data=employee_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Employee added successfully.", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            employee_data = request.data
            employee = get_object_or_404(Employee, employeeID=id)
            serializer = EmployeeSerializer(employee, data=employee_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Employee updated successfully.", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            employee = get_object_or_404(Employee, employeeID=id)
            employee.delete()
            return Response("Employee deleted successfully.", status=status.HTTP_204_NO_CONTENT)

    except Employee.DoesNotExist:
        return HttpResponseNotFound("Employee not found")


# Employee List Create View
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# Employee Retrieve Update Destroy View
class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# Save File View
@api_view(['POST'])
@parser_classes([JSONParser])
def save_file(request):
    try:
        file = request.FILES['file']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        return Response(f"File '{file_name}' saved successfully.", status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# Poste Views
class PosteListCreateView(generics.ListCreateAPIView):
    queryset = Poste.objects.all()
    serializer_class = PosteSerializer


class PosteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poste.objects.all()
    serializer_class = PosteSerializer


def create_poste(request):
    if request.method == 'POST':
        form = PosteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('poste_list')
    else:
        form = PosteForm()

    return render(request, 'create_poste.html', {'form': form})


def view_poste(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    return render(request, 'view_poste.html', {'poste': poste})


def update_poste(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)

    if request.method == 'POST':
        form = PosteForm(request.POST, instance=poste)
        if form.is_valid():
            form.save()
            return redirect('poste_list')
    else:
        form = PosteForm(instance=poste)

    return render(request, 'update_poste.html', {'form': form})


def delete_poste(request, poste_id):
    poste = get_object_or_404(Poste, pk=poste_id)
    poste.delete()
    return redirect('poste_list')


# Competence Views
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def competence_api(request, id=0):
    try:
        if request.method == 'GET':
            competences = Competence.objects.all()
            serializer = CompetenceSerializer(competences, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            competence_data = request.data
            serializer = CompetenceSerializer(data=competence_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Competence added successfully.", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            competence_data = request.data
            competence = get_object_or_404(Competence, id=id)
            serializer = CompetenceSerializer(competence, data=competence_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Competence updated successfully.", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            competence = get_object_or_404(Competence, id=id)
            competence.delete()
            return Response("Competence deleted successfully.", status=status.HTTP_204_NO_CONTENT)

    except Competence.DoesNotExist:
        return HttpResponseNotFound("Competence not found")


# Tache Views
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def tache_api(request, id=0):
    try:
        if request.method == 'GET':
            taches = Tache.objects.all()
            serializer = TacheSerializer(taches, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            tache_data = request.data
            serializer = TacheSerializer(data=tache_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Tache ajouté avec succès.", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            tache_data = request.data
            tache = get_object_or_404(Tache, id=id)
            serializer = TacheSerializer(tache, data=tache_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Tache màj avec succès", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            tache = get_object_or_404(Tache, id=id)
            tache.delete()
            return Response("Tache deleted successfully.", status=status.HTTP_204_NO_CONTENT)

    except Tache.DoesNotExist:
        return HttpResponseNotFound("Tache n'éxiste pas")


# Tache List Create View
class TacheListCreateView(generics.ListCreateAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer


# Tache Retrieve Update Destroy View
class TacheRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer


# Equipe Views
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def equipe_api(request, id=0):
    try:
        if request.method == 'GET':
            equipes = Equipe.objects.all()
            serializer = EquipeSerializer(equipes, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = EquipeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Equipe ajouté.", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            equipe = get_object_or_404(Equipe, id=id)
            serializer = EquipeSerializer(equipe, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Equipe màj.", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            equipe = get_object_or_404(Equipe, id=id)
            equipe.delete()
            return Response("Equipe supprimé!", status=status.HTTP_204_NO_CONTENT)

    except Equipe.DoesNotExist:
        return HttpResponseNotFound("Equipe not found")


# Onboarding Views
class OnboardingListCreateView(generics.ListCreateAPIView):
    queryset = Onboarding.objects.all()
    serializer_class = OnboardingSerializer


class OnboardingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Onboarding.objects.all()
    serializer_class = OnboardingSerializer


# Etape Onboarding Views
class EtapeOnboardingListCreateView(generics.ListCreateAPIView):
    queryset = EtapeOnboarding.objects.all()
    serializer_class = EtapeOnboardingSerializer


class EtapeOnboardingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EtapeOnboarding.objects.all()
    serializer_class = EtapeOnboardingSerializer


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def onboarding_api(request, id=0):
    try:
        if request.method == 'GET':
            onboarding_instances = Onboarding.objects.all()
            serializer = OnboardingSerializer(onboarding_instances, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            onboarding_data = request.data
            serializer = OnboardingSerializer(data=onboarding_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Onboarding.DoesNotExist:
        return HttpResponseNotFound("Onboarding not found")


# Etape Onboarding API
@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def etape_onboarding_api(request, onboarding_id):
    try:
        onboarding = get_object_or_404(Onboarding, id=onboarding_id)

        if request.method == 'GET':
            etapes = onboarding.etapes.all()
            serializer = EtapeOnboardingSerializer(etapes, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            etape_data = request.data
            etape_data['onboarding'] = onboarding.id
            serializer = EtapeOnboardingSerializer(data=etape_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Etape ajouté.", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Onboarding.DoesNotExist:
        return HttpResponseNotFound("Onboarding not found")


@api_view(['PUT', 'DELETE'])
@parser_classes([JSONParser])
def etape_onboarding_detail_api(request, onboarding_id, etape_id):
    try:
        onboarding = get_object_or_404(Onboarding, id=onboarding_id)
        etape = onboarding.etapes.get(id=etape_id)

        if request.method == 'PUT':
            etape_data = request.data
            serializer = EtapeOnboardingSerializer(etape, data=etape_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Etape màj.", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            etape.delete()
            return Response("Etape supprimé.", status=status.HTTP_204_NO_CONTENT)

    except (Onboarding.DoesNotExist, EtapeOnboarding.DoesNotExist):
        return HttpResponseNotFound("Onboarding ou l'Etape n'existe pas")


@api_view(['GET'])
@parser_classes([JSONParser])
def etape_onboarding_list_api(request, onboarding_id):
    try:
        onboarding = get_object_or_404(Onboarding, id=onboarding_id)
        etapes = onboarding.etapes.all()
        serializer = EtapeOnboardingSerializer(etapes, many=True)
        return Response(serializer.data)

    except Onboarding.DoesNotExist:
        return Response({"error": "Onboarding not found"}, status=404)


@api_view(['POST'])
@parser_classes([JSONParser])
def assign_competence_to_employee(request, employee_id, competence_id):
    try:
        employee = get_object_or_404(Employee, id=employee_id)
        competence = get_object_or_404(Competence, id=competence_id)

        if request.method == 'POST':
            employee_competence_data = {'employee': employee.id, 'competence': competence.id}
            serializer = EmployeeCompetenceSerializer(data=employee_competence_data)

            if serializer.is_valid():
                serializer.save()
                return Response("Competence assigned to employee successfully.", status=201)

            return Response(serializer.errors, status=400)

    except (Employee.DoesNotExist, Competence.DoesNotExist):
        return HttpResponseNotFound("Employee or Competence not found")


# Affectation Views
class AffectationListCreateView(generics.ListCreateAPIView):
    queryset = Affectation.objects.all()
    serializer_class = AffectationSerializer

    def post(self, request, *args, **kwargs):
        serializer = AffectationSerializer(data=request.data)

        if serializer.is_valid():
            # Validate the data, including the total ratio sum
            serializer.validate(request.data)
            # Save the affectation
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Employment History Views
class EmploymentHistoryListCreateView(generics.ListCreateAPIView):
    queryset = EmploymentHistory.objects.all()
    serializer_class = EmploymentHistorySerializer


class EmploymentHistoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmploymentHistory.objects.all()
    serializer_class = EmploymentHistorySerializer


@api_view(['GET'])
@parser_classes([JSONParser])
def search_employee(request):
    try:
        # Get the query parameters from the request
        name = request.query_params.get('name')
        position = request.query_params.get('position')

        # Initialize queryset
        queryset = Employee.objects.all()

        # Filter employees by name if provided
        if name:
            queryset = queryset.filter(firstName__icontains=name) | queryset.filter(lastName__icontains=name)

        # Filter employees by position if provided
        if position:
            queryset = queryset.filter(position__icontains=position)

        # Serialize the results using EmployeeSerializer
        serializer = EmployeeSerializer(queryset, many=True)

        return Response(serializer.data)

    except Employee.DoesNotExist:
        return HttpResponseNotFound("Employee not found")



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':

        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
        else:
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)


        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)


        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)

            return JsonResponse({'success': 'Login successful'}, status=200)
        else:

            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)


from django.shortcuts import redirect
from django.contrib.auth import logout
@csrf_exempt
def custom_logout(request):

    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=200)
    else:
        return JsonResponse({'error': 'User not logged in'}, status=400)


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser

@csrf_exempt
def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        try:

            data = json.loads(request.body)


            custom_user_data = data.get('CustomUser', {})


            username = custom_user_data.get('username', None)
            email = custom_user_data.get('email', None)
            password = custom_user_data.get('password', None)


            if not username or not email or not password:
                return JsonResponse({'errors': 'All fields are required'}, status=400)

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'errors': 'Email address already exists'}, status=400)


            user = CustomUser.objects.create_user(username=username, email=email, password=password)


            user.first_name = custom_user_data.get('first_name', '')
            user.last_name = custom_user_data.get('last_name', '')
            user.date_of_birth = custom_user_data.get('date_of_birth', None)
          
            user.save()

            return JsonResponse({'message': 'User registered successfully'}, status=201)

        except json.JSONDecodeError as e:
            return JsonResponse({'errors': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'errors': str(e)}, status=400)

    return JsonResponse({'errors': 'Invalid request method'}, status=405)