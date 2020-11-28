from .models import Candidate, Employer, JobPosting

class Match:
    def __init__(self, u):
        self.user = u

    def count_common(self, a, b):
        a_set = set(a)
        b_set = set(b)
        a_set = (a_set & b_set)
        return len(a_set)

    def the_matchmaker(self):
        candidate = Candidate.objects.filter(user=self.user)[0]
        jobs = JobPosting.objects.all()
        possible_jobs = []
        for job in jobs:
            points = 0
            if (job.job_title==candidate.job_role) and (job.salary_per_annum>=candidate.salary_req) and (job.exp_in_yrs<=candidate.experience):
                points = points+(candidate.experience-job.exp_in_yrs)
                if(job.get_skill_index()!=[]):
                    points = points+self.count_common(job.get_skill_index(), candidate.get_skill_index())
                possible_jobs.append([job, points])
        
        possible_jobs.sort(reverse=True,key = lambda x: x[1])
        if len(possible_jobs)<=3:
            return possible_jobs
        return possible_jobs[0:3]

    def employer_matchmaker(self, candidates, job):
        top_candidates = []
        for candidate in candidates:
            points = 0
            if (job.job_title==candidate.job_role) and (job.salary_per_annum>=candidate.salary_req) and (job.exp_in_yrs<=candidate.experience):
                points = points+(candidate.experience-job.exp_in_yrs)
                if(candidate.get_skill_index()!=[]):
                    points = points+self.count_common(job.get_skill_index(), candidate.get_skill_index())
                top_candidates.append([candidate, points])
        
        top_candidates.sort(reverse=True,key = lambda x: x[1])
        new_list = []
        for l in top_candidates:
            new_list.append(l[0])
        if len(new_list)<=3:
            return new_list
        return new_list[0:3]
        