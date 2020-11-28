from django.contrib import admin
from .models import Candidate, Employer, JobPosting
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Employer)
admin.site.register(JobPosting)