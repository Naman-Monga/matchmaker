from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import JobPosting, Candidate, Employer, skills_list, job_list
from .decorators import allowed_users
from .forms import PersonalInfoForm, JobSpecsForm, JobPostingForm
import json
from django.contrib import messages
from .matchmaker import Match
# Create your views here.

def home(request):
    jobs = JobPosting.objects.all()
    employee = False
    if request.user.is_authenticated:    
        if request.user.groups.all()[0].name == 'Employee':
            employee = True

    if request.method=="POST":
        jobtitle = request.POST.get('jobtitle')
        if jobtitle:
            jobs = jobs.filter(job_title__icontains=jobtitle)
        minsal = request.POST.get('minsal')
        if minsal:
            jobs = jobs.filter(salary_per_annum__gte=float(minsal))
    context = {
        'jobs':jobs,
        'employee':employee,
    }
    return render(request,'core/index.html', context)

@allowed_users(['Employer'])
def comp_dashboard(request):
    form = JobPostingForm()
    employee = False
    if request.user.groups.all()[0].name == 'Employee':
        employee = True
    if request.method=='POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_title = form.cleaned_data.get('job_title')
            job_description = form.cleaned_data.get('job_description')
            salary_per_annum = form.cleaned_data.get('salary_per_annum')
            experience_required = form.cleaned_data.get('experience_required')
            date_deadline = form.cleaned_data.get('date_deadline')
            skills_req = form.cleaned_data.get('skills_req')
            new_job = JobPosting(
                employer=Employer.objects.filter(user = request.user)[0], 
                job_description=job_description,
                salary_per_annum=salary_per_annum,
                exp_in_yrs=experience_required,
                date_deadline=date_deadline,
            )
            mylist = []
            for skill in  skills_req:
                for i in skills_list:
                    if skill == i[0]:
                        mylist.append(i[1])
                        break
            new_job.skills = json.dumps(mylist)
            new_job.set_job_title(job_title)
            new_job.save()
            messages.success(request, 'Job Posted Successfully!')
            return redirect('company-dashboard')
    context = {
        'job_form':form,
        'employee':employee,
    }
    return render(request, 'core/employerPanel.html', context)

@allowed_users(["Employee"])
def empl_dashboard(request):
    candidate = Candidate.objects.filter(user = request.user)[0]
    employee = False
    if request.user.groups.all()[0].name == 'Employee':
        employee = True
    my_specs = {}
    my_info = {}
    if candidate.skills:
        my_info = {
            'skills':candidate.get_skill_index(),
            'experience':candidate.experience,
        }
    if candidate.salary_req:
        my_specs = {
            'salary_req':candidate.salary_req,
            'job_type':candidate.get_job_index(),
        }
    info_form = PersonalInfoForm(initial=my_info)
    specs_form = JobSpecsForm(initial=my_specs)
    if request.method=="POST":
        specs_form = JobSpecsForm(request.POST)
        if specs_form.is_valid():
            sal = specs_form.cleaned_data.get('salary_req')
            jt = specs_form.cleaned_data.get('job_type')
            candidate.salary_req = sal
            for job in job_list:
                if job[0]==jt:
                    jt = job[1]
                    break
            candidate.job_role = jt
            candidate.save()
            return redirect('my-dashboard')

    context = {
        'candidate':candidate,
        'specs_form':specs_form,
        'info_form':info_form,
        'employee':employee,
    }
    return render(request, 'core/employeePanel.html', context)


def info_form_view(request):
    candidate = Candidate.objects.filter(user=request.user)[0]
    employee = False
    if request.user.is_authenticated:
        if request.user.groups.all()[0].name == 'Employee':
            employee = True
    if request.method=="POST":
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            skills = form.cleaned_data.get('skills')
            exp = form.cleaned_data.get('experience')
            candidate.experience = exp
            mylist = []
            for skill in  skills:
                for i in skills_list:
                    if skill == i[0]:
                        mylist.append(i[1])
                        break
            candidate.skills = json.dumps(mylist)
            candidate.save()
    context = {
        'employee':employee
    }
    return render(request, 'my-dashboard', context)
    
@login_required(login_url='login')
def match_view(request):
    match = Match(request.user)
    the_list = match.the_matchmaker()
    new_list = []
    for l in the_list:
        new_list.append(l[0])
        
    context= {
        'matches':new_list,
    }
    return render(request, 'core/matchmaker.html',context)

@login_required(login_url='login')
def job_detail_view(request, jobid):
    # TODO: Dont show apply button when company owner visits the page.
    the_job = JobPosting.objects.get(id=jobid)
    is_owner = False
    applications = []
    employee = Candidate.objects.get(user=request.user)
    applied = False
    top_candidates = []
    is_top=False
    for group in request.user.groups.all():
        if(group.name=="Employer"):
            employer = Employer.objects.get(user = request.user)
            if the_job.employer==employer:
                is_owner = True
                applications = the_job.applications.all()
                print(applications)
                print(the_job)
                if len(applications):
                    top_candidates = Match(request.user).employer_matchmaker(applications,the_job)
                if len(top_candidates):
                    is_top = True
    if employee in the_job.applications.all():
        applied = True
    if request.method=="POST":
        if request.POST.get('confirm')=='apply' and not applied:
            the_job.applications.add(employee)
            return redirect('job-detail', jobid)

    context = {
        'job':the_job,
        'applied':applied,
        'is_owner':is_owner,
        'applications':applications,
        'top_candidates':top_candidates,
        'is_top':is_top,
    }
    return render(request, 'core/jobDetail.html', context)


def jobs_posted(request):
    employer_here = Employer.objects.get(user = request.user)
    jobs = JobPosting.objects.filter(employer = employer_here)
    context = {
        'jobs':jobs,
    }
    return render(request, 'core/jobsPosted.html', context)

def jobs_applied(request):
    employee_here = Candidate.objects.get(user = request.user)
    jobs = []
    for job in JobPosting.objects.all():
        if employee_here in job.applications.all():
            jobs.append(job)
    context = {
        'jobs':jobs,
    }
    return render(request, 'core/jobsApplied.html', context)