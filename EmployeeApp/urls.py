from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view

from . import views
from .views import (
    department_api,
    EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView,
    PosteListCreateView, PosteRetrieveUpdateDestroyView,
    OnboardingListCreateView, OnboardingRetrieveUpdateDestroyView,
    EtapeOnboardingListCreateView, EtapeOnboardingRetrieveUpdateDestroyView,
    save_file, assign_competence_to_employee, competence_api, TacheListCreateView, TacheRetrieveUpdateDestroyView,
    AffectationListCreateView, EmploymentHistoryListCreateView, EmploymentHistoryRetrieveUpdateDestroyView,
     etape_onboarding_list_api, equipe_api
)

urlpatterns = [
    # Department URLs
    path('api/department/', department_api, name='department-api'),
    path('api/department/<int:id>/', department_api, name='department-api-detail'),

    # Employee URLs
    path('api/employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('api/employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-retrieve-update-destroy'),

    # Poste URLs
    path('api/postes/', PosteListCreateView.as_view(), name='poste-list-create'),
    path('api/postes/<int:pk>/', PosteRetrieveUpdateDestroyView.as_view(), name='poste-retrieve-update-destroy'),

    # Onboarding URLs
    path('api/onboarding/', OnboardingListCreateView.as_view(), name='onboarding-list-create'),
    path('api/onboarding/<int:pk>/', OnboardingRetrieveUpdateDestroyView.as_view(), name='onboarding-retrieve-update-destroy'),

    # EtapeOnboarding URLs
    path('api/etapeonboarding/', EtapeOnboardingListCreateView.as_view(), name='etapeonboarding-list-create'),
    path('api/etapeonboarding/<int:pk>/', EtapeOnboardingRetrieveUpdateDestroyView.as_view(), name='etapeonboarding-retrieve-update-destroy'),
    # EtapeOnboarding URLs associated with Onboarding
    path('api/onboarding/<int:onboarding_id>/etapeonboarding/', views.etape_onboarding_list_api,
         name='etapeonboarding-list-for-onboarding'),
    path('etape-onboarding-list/<int:onboarding_id>/', etape_onboarding_list_api),
    # Competence URL
    path('api/competences/', competence_api, name='competence-api'),

    path('api/employees/<int:employee_id>/competences/<int:competence_id>/', assign_competence_to_employee,
         name='assign-competence-to-employee'),

    path('api/taches/', TacheListCreateView.as_view(), name='tache-list-create'),
    path('api/taches/<int:pk>/', TacheRetrieveUpdateDestroyView.as_view(), name='tache-retrieve-update-destroy'),
    #Equipe

    path('equipe-api/', equipe_api, name='equipe_api'),
    path('equipe-api/<int:id>/', equipe_api, name='equipe_api_detail'),


 # Employment History URLs
    path('api/employment-history/', EmploymentHistoryListCreateView.as_view(), name='employment-history-list-create'),
    path('api/employment-history/<int:pk>/', EmploymentHistoryRetrieveUpdateDestroyView.as_view(),
         name='employment-history-detail'),

    path('api/search/employee/', views.search_employee, name='search_employee'),


    # Other URLs
    re_path(r'employee/', views.employee_api),
    re_path(r'SaveFile/', save_file),
    path('api/affectations/', AffectationListCreateView.as_view(), name='affectation-list-create'),


    path('api-auth/', include('rest_framework.urls'))

]


