from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as auth_views
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
    path('department/', department_api, name='department-api'),
    path('department/<int:id>/', department_api, name='department-api-detail'),

    # Employee URLs
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-retrieve-update-destroy'),

    # Poste URLs
    path('postes/', PosteListCreateView.as_view(), name='poste-list-create'),
    path('postes/<int:pk>/', PosteRetrieveUpdateDestroyView.as_view(), name='poste-retrieve-update-destroy'),

    # Onboarding URLs
    path('onboarding/', OnboardingListCreateView.as_view(), name='onboarding-list-create'),
    path('onboarding/<int:pk>/', OnboardingRetrieveUpdateDestroyView.as_view(),
         name='onboarding-retrieve-update-destroy'),

    # EtapeOnboarding URLs
    path('etapeonboarding/', EtapeOnboardingListCreateView.as_view(), name='etapeonboarding-list-create'),
    path('etapeonboarding/<int:pk>/', EtapeOnboardingRetrieveUpdateDestroyView.as_view(),
         name='etapeonboarding-retrieve-update-destroy'),

    # EtapeOnboarding URLs associated with Onboarding
    path('onboarding/<int:onboarding_id>/etapeonboarding/', views.etape_onboarding_list_api,
         name='etapeonboarding-list-for-onboarding'),
    path('etape-onboarding-list/<int:onboarding_id>/', etape_onboarding_list_api),

    # Competence URL
    path('competences/', competence_api, name='competence-api'),

    path('employees/<int:employee_id>/competences/<int:competence_id>/', assign_competence_to_employee,
         name='assign-competence-to-employee'),

    path('taches/', TacheListCreateView.as_view(), name='tache-list-create'),
    path('taches/<int:pk>/', TacheRetrieveUpdateDestroyView.as_view(), name='tache-retrieve-update-destroy'),

    # Equipe
    path('equipe-api/', equipe_api, name='equipe_api'),
    path('equipe-api/<int:id>/', equipe_api, name='equipe_api_detail'),

    # Employment History URLs
    path('employment-history/', EmploymentHistoryListCreateView.as_view(), name='employment-history-list-create'),
    path('employment-history/<int:pk>/', EmploymentHistoryRetrieveUpdateDestroyView.as_view(),
         name='employment-history-detail'),

    path('search/employee/', views.search_employee, name='search_employee'),

    # Other URLs
    re_path(r'employee/', views.employee_api),
    re_path(r'SaveFile/', save_file),
    path('affectations/', AffectationListCreateView.as_view(), name='affectation-list-create'),




    path('accounts/', include('django.contrib.auth.urls')),

    #Logreg
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),

]
