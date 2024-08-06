from django.db import models
from django.utils import timezone

# user master table
class UserMaster(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    role = models.CharField(max_length=50, default='candidate')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)

# candidate table
class Candidate(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    dob = models.CharField()
    about = models.CharField(max_length=150)
    gender = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='images/candidates/')
    resume = models.FileField(upload_to='resume/candidates/', default='null')

# company table
class Company(models.Model):
    user_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    about = models.CharField(max_length=350, default='null')
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    website = models.CharField(max_length=50, default='null')
    profile_pic = models.ImageField(upload_to='images/companies/')

# job table
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1550)
    responsibilities = models.CharField(max_length=1550)
    qualification = models.CharField(max_length=1550)
    date_posted = models.DateTimeField(default=timezone.now)
    experience = models.CharField(max_length=50)
    salary = models.IntegerField()
    location = models.CharField(max_length=50, default='null')
    vacancy = models.IntegerField(default=10)
    deadline = models.CharField(max_length=50, default='null')
    type = models.CharField(max_length=50, default='null')
    number_of_applicants = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='active')

# job application table
class JobApplication(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='pending')
