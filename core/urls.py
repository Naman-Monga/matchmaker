from django.urls import path
from .views import home, comp_dashboard, empl_dashboard, info_form_view, job_detail_view, match_view, jobs_posted, jobs_applied


urlpatterns = [
    path('', home,name = "home"),
    path('company-dashboard/',comp_dashboard, name="company-dashboard"),
    path('my-dashboard/',empl_dashboard, name="my-dashboard"),
    path('info-form/',info_form_view, name="info-form"),
    path('matchmaker/',match_view, name="matchmaker"),
    path('jobs-posted', jobs_posted, name='jobs-posted'),
    path('job-detail/<str:jobid>/', job_detail_view, name='job-detail'),
    path('jobs-applied/', jobs_applied, name="jobs-applied")
]

