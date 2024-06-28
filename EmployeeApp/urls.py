# urls.py
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    OnboardingViewSet, EtapeOnboardingViewSet, TaskViewSet, NotificationViewSet, OnboardingProgressViewSet,
    sign_in_with_token, get_current_user, department_api, EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView,
    PosteListCreateView, PosteRetrieveUpdateDestroyView, save_file, assign_competence_to_employee,
    competence_api, TacheListCreateView, TacheRetrieveUpdateDestroyView, AffectationListCreateView,
    EmploymentHistoryListCreateView, EmploymentHistoryRetrieveUpdateDestroyView, etape_onboarding_list_api, equipe_api
)

router = DefaultRouter()
router.register(r'onboardings', OnboardingViewSet)
router.register(r'etapes', EtapeOnboardingViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'onboarding-progress', OnboardingProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Department URLs
    path('department/', department_api, name='department-api'),
    path('department/<int:id>/', department_api, name='department-api-detail'),

    # Employee URLs
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-retrieve-update-destroy'),

    # Poste URLs
    path('create-poste/', views.create_poste, name='create_poste'),
    path('update-poste/<int:pk>/', views.update_poste, name='update_poste'),
    path('close-poste/<int:pk>/', views.close_poste, name='close_poste'),



    # EtapeOnboarding URLs associated with Onboarding
    path('onboarding/<int:onboarding_id>/etapeonboarding/', views.etape_onboarding_list_api, name='etapeonboarding-list-for-onboarding'),
    path('etape-onboarding-list/<int:onboarding_id>/', etape_onboarding_list_api),

    # Competence URL
    path('competences/', competence_api, name='competence-api'),
    path('employees/<int:employee_id>/competences/<int:competence_id>/', assign_competence_to_employee, name='assign-competence-to-employee'),

    # Task URLs
    path('taches/', TacheListCreateView.as_view(), name='tache-list-create'),
    path('taches/<int:pk>/', TacheRetrieveUpdateDestroyView.as_view(), name='tache-retrieve-update-destroy'),

    # Equipe
    path('equipe-api/', equipe_api, name='equipe_api'),
    path('equipe-api/<int:id>/', equipe_api, name='equipe_api_detail'),

    # Employment History URLs
    path('employment-history/', EmploymentHistoryListCreateView.as_view(), name='employment-history-list-create'),
    path('employment-history/<int:pk>/', EmploymentHistoryRetrieveUpdateDestroyView.as_view(), name='employment-history-detail'),

    # Other URLs
    path('search/employee/', views.search_employee, name='search_employee'),
    re_path(r'employee/', views.employee_api),
    re_path(r'SaveFile/', save_file),
    path('affectations/', AffectationListCreateView.as_view(), name='affectation-list-create'),

    path('accounts/', include('django.contrib.auth.urls')),

    # Authentication URLs
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('register/', views.register, name='register'),
    path('current_user/', views.get_current_user, name='get_current_user'),
    path('auth/sign-in-with-token/', sign_in_with_token, name='sign_in_with_token'),

    # Contract URLs
    path('contract-types/', views.contract_type_list, name='contract_type_list'),
    path('contract-types/<int:pk>/', views.contract_type_detail, name='contract_type_detail'),
    path('contracts/', views.contract_list, name='contract_list'),
    path('contracts/<int:pk>/', views.contract_detail, name='contract_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
