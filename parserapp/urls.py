from django.urls import path
from .views import *

urlpatterns = [
    path('', PaShowResultsVacancies.as_view(), name='pr_result_vacancies_url'),
    path('resumes/', PaShowResultsResumes.as_view(), name='pr_result_resumes_url'),
    path('refreshdbvacancies/', PaRefreshdbVacancies.as_view(), name='pr_refreshdb_vacancies_url'),
    path('refreshdbresumes/', PaRefreshdbResumes.as_view(), name='pr_refreshdb_resumes_url'),
]