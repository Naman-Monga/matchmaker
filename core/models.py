from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.
class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 300)
    description = models.CharField(max_length = 1000)

    def __str__(self):
        return self.name
    
skills_list = [
    ('0', 'python'),
    ('1', 'javascript'),
    ('2', 'msql'),
    ('3', 'docker'),
    ('4', 'AWS'),
]

job_list = [
    ('0', 'SDE1'),
    ('1', 'Full Stack Dev'),
    ('2', 'Manager'),
    ('3', 'Designer'),
]

class Candidate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length = 300, null=True, blank = True)
    lname = models.CharField(max_length = 300, null=True, blank = True)
    # personal info
    skills = models.CharField(max_length = 300,  null = True, blank = True)
    experience = models.IntegerField(null=True, blank = True)
    # job requirements
    salary_req = models.FloatField(null=True, blank = True)
    job_role = models.CharField(max_length = 300, null=True, blank=True)

    def __str__(self):
        return self.fname
    
    def get_skill_index(self):
        thelist = []
        jsonDec = json.decoder.JSONDecoder()
        skilly = jsonDec.decode(self.skills)
        for skill in skilly:
            for s in skills_list:
                if skill==s[1]:
                    thelist.append(s[0])
        return thelist

    def get_job_index(self):
        for job in job_list:
            if job[1]==self.job_role:
                return job[0] 


class JobPosting(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    applications = models.ManyToManyField(Candidate, blank=True)
    job_description = models.CharField(max_length = 2000)
    job_title = models.CharField(max_length = 300)
    salary_per_annum = models.FloatField()
    exp_in_yrs = models.FloatField()
    date_created = models.DateTimeField(auto_now=True)
    date_deadline = models.DateField()
    skills = models.CharField(max_length=1000,null=True)

    def __str__(self):
        return self.job_title

    def set_job_title(self, job_index):
        for job in job_list:
            if job_index==job[0]:
                self.job_title=job[1]

    def get_skill_index(self):
        thelist = []
        jsonDec = json.decoder.JSONDecoder()
        skilly = jsonDec.decode(self.skills)
        for skill in skilly:
            for s in skills_list:
                if skill==s[1]:
                    thelist.append(s[0])
        return thelist