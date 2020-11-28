from django import forms
from .models import Candidate, skills_list, job_list
import datetime
exp_list = [
    ('0', 'less than 1 year'),
    ('1', '1-2 yrs'),
    ('2', '2+ yrs'),
    ('3', '3+ yrs'),
    ('4', '4+ yrs'),
    ('5', '5+ yrs'),
]



class PersonalInfoForm(forms.Form):
    skills = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices = skills_list)
    experience = forms.ChoiceField(choices = exp_list)

class JobSpecsForm(forms.Form):
    salary_req = forms.FloatField()
    job_type = forms.ChoiceField(choices=job_list)

class JobPostingForm(forms.Form):
    job_title = forms.ChoiceField(choices=job_list)
    job_description = forms.CharField(max_length=300)
    salary_per_annum = forms.FloatField()
    experience_required = forms.ChoiceField(choices = exp_list)
    date_deadline = forms.DateField(initial=datetime.date.today)
    skills_req = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices = skills_list)

class SearchForm(forms.Form):
    job_title = forms.CharField(max_length=300)
    experience = forms.CharField(max_length=200)