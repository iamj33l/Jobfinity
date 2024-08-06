import re
import uuid
from datetime import datetime
from .utils import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')


def signIn(request):
    request.session.clear()
    return render(request, 'signIn.html')


def jobList(request):
    # get data and shuffle it
    jobs = Job.objects.filter(status='active').order_by('salary')
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_page = page_obj.paginator.num_pages
    return render(request, 'jobList.html', {'jobs': page_obj, 'total_page': total_page})

def tokenSent(request):
    return render(request, 'tokenSent.html')


def verified(request):
    return render(request, 'verified.html')

def companyProfile(request):
    company = Company.objects.get(id=request.session['id'])
    return render(request, 'companyProfile.html', {'company': company})

def postJob(request):
    return render(request, 'postJob.html')

# view to register(sign up) user
def register_attempt(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')

        try:
            # check if email already exists
            if UserMaster.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'})

            # check for empty fields
            if not email or not password or not role:
                return JsonResponse({'error': 'All fields are required'})

            # check for password validation with regex
            if not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', password):
                messages.error(request,
                               'Password must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 numeric and 1 special character')
                return JsonResponse({'error': 'Password must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 numeric and 1 special character'})

            # create token
            token = str(uuid.uuid4())

            # create user
            user = UserMaster.objects.create(
                email=email,
                password=password,
                token=token,
                role=role
            )
            user.save()
            if role.lower() == 'company':
                company = Company.objects.create(user_id=user, company_name=name)
                company.save()

            if role.lower() == 'candidate':
                candidate = Candidate.objects.create(user_id=user, firstname=(name.split(' ')[0]),
                                                     lastname=(name.split(' ')[1]))
                candidate.save()

            # send verification email
            send_verification_email(name, email, token)
            return JsonResponse({'success': 'Account created successfully. Please check your emails and verify your email to login'})

        except Exception as e:
            print(e)

    return redirect('signIn')


def verify(request, token):
    try:
        user = UserMaster.objects.get(token=token)

        if user:
            if user.is_verified:
                return redirect('verified')
            else:
                user.is_verified = True
                user.save()
                return redirect('verified')
        else:
            return redirect('signIn')

    except UserMaster.DoesNotExist:
        return redirect('signIn')
    except Exception as e:
        print(e)
        return redirect('signIn')


def login_attempt(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            if UserMaster.objects.filter(email=email).exists():
                user = UserMaster.objects.get(email=email)
                if user.password == password:
                    if user.is_verified:
                        if user.role == 'candidate':
                            candidate = Candidate.objects.get(user_id=user)
                            request.session['id'] = candidate.id
                            request.session['name'] = candidate.firstname + ' ' + candidate.lastname
                            request.session['email'] = user.email
                            request.session['role'] = user.role
                            request.session['is_signed_in'] = True
                            return JsonResponse({'success': 'Login successful'})

                        if user.role == 'company':
                            company = Company.objects.get(user_id=user)
                            request.session['id'] = company.id
                            request.session['name'] = company.company_name
                            request.session['email'] = user.email
                            request.session['role'] = user.role
                            request.session['is_signed_in'] = True
                            return JsonResponse({'success': 'Login successful'})
                    else:
                        messages.error(request, 'Please verify your account to login')
                        return JsonResponse({'error': 'Please verify your account to login'})
                else:
                    messages.error(request, 'Incorrect password')
                    return JsonResponse({'error': 'Incorrect password'})
            else:
                messages.error(request, 'Email does not exist')
                return JsonResponse({'error': 'Email does not exist'})

        except Exception as e:
            print(e)
            return redirect('signIn')

    return redirect('signIn')

# view to post a job
def post_job_attempt(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        responsibilities = request.POST['responsibilities']
        qualification = request.POST['qualification']
        experience = request.POST['experience']
        salary = request.POST['salary']
        location = request.POST['location']
        deadline = request.POST['deadline']
        type = request.POST['type']
        vacancy = request.POST['vacancy']
        status = 'active'

        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        today = datetime.now().date()
        if deadline_date < today:
            status = 'inactive'

        try:
            if request.session['is_signed_in']:
                company = Company.objects.get(id=request.session['id'])
                job = Job.objects.create(
                    company=company,
                    title=title,
                    description=description,
                    responsibilities=responsibilities,
                    qualification=qualification,
                    experience=experience,
                    salary=salary,
                    location=location,
                    deadline=deadline,
                    type=type,
                    vacancy=vacancy,
                    status=status
                )
                job.save()
                return JsonResponse({'success': 'Job posted successfully'})
            else:
                return JsonResponse({'error': 'Please login to post a job'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred while posting the job'})

    return JsonResponse({'error': 'An error occurred while posting the job'})

# view to update a job
def update_job(request, primary_key):
    job_data = Job.objects.get(id=primary_key)
    return render(request, 'updateJob.html', {'job': job_data})

def update_job_attempt(request, primary_key):
    if request.method == 'POST':
        try:
            if request.session['is_signed_in']:
                job = Job.objects.get(id=primary_key)
                job.title = request.POST['title']
                job.description = request.POST['description']
                job.responsibilities = request.POST['responsibilities']
                job.qualification = request.POST['qualification']
                job.experience = request.POST['experience']
                job.location = request.POST['location']
                job.salary = request.POST['salary']
                job.type = request.POST['type']
                job.deadline = request.POST['deadline']
                job.vacancy = request.POST['vacancy']
                job.save()
                deadline_date = datetime.strptime(job.deadline, '%Y-%m-%d').date()
                today = datetime.now().date()
                if deadline_date < today:
                    job.status = 'inactive'
                else:
                    job.status = 'active'

                job.save()
                return JsonResponse({'success': 'Job updated successfully'})
            else:
                return JsonResponse({'error': 'Please login to update a job'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred while updating the job'})

    return JsonResponse({'error': 'An error occurred while updating the job'})

def applyJob(request, primary_key):
    is_applied = False
    job = Job.objects.get(id=primary_key)
    if request.session['is_signed_in']:
        candidate = Candidate.objects.get(id=request.session['id'])
        if JobApplication.objects.filter(candidate=candidate, job=job).exists():
            is_applied = True
    else:
        return JsonResponse({'error': 'Please login to apply for a job'})
    return render(request, 'applyJob.html', {'job': job, 'is_applied': is_applied})

def apply_job_attempt(request, primary_key):
    if request.method == 'POST':
        try:
            if request.session['is_signed_in']:
                job = Job.objects.get(id=primary_key)
                candidate = Candidate.objects.get(id=request.session['id'])
                application = JobApplication.objects.create(job=job, candidate=candidate)
                job.number_of_applicants += 1
                job.save()
                application.save()
                return JsonResponse({'success': 'Applied for job successfully'})
            else:
                return JsonResponse({'error': 'Please login to apply for job'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred while applying for Job'})
    else:
        return JsonResponse({'error': 'An error occurred while applying for job'})

def companyDashboard(request):
    jobs = Job.objects.filter(company_id=request.session['id'])
    return render(request, 'companyDashboard.html', {'jobs': jobs})

def candidateDashboard(request):
    candidate = Candidate.objects.get(id=request.session['id'])
    applications = JobApplication.objects.filter(candidate=candidate)
    return render(request, 'candidateDashboard.html', {'applications': applications})

def applicantsTable(request, primary_key):
    job = Job.objects.get(id=primary_key)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'applicantsTable.html', {'applications': applications})

def candidateProfile(request):
    candidate = Candidate.objects.get(id=request.session['id'])
    return render(request, 'candidateProfile.html', {'candidate': candidate})

def edit_candidate_profile(request, primary_key):
    candidate = Candidate.objects.get(id=primary_key)
    return render(request, 'editCandidateProfile.html', {'candidate': candidate})


def edit_candidate_profile_attempt(request, primary_key):
    if request.method == 'POST':
        try:
            if request.session['is_signed_in']:
                candidate = Candidate.objects.get(id=primary_key)
                if 'profile' in request.FILES:
                    candidate.profile_pic = request.FILES['profile']
                candidate.firstname = request.POST['firstname']
                candidate.lastname = request.POST['lastname']
                candidate.about = request.POST['about']
                candidate.gender = request.POST['gender']
                candidate.dob = request.POST['dob']
                candidate.contact = request.POST['contact']
                candidate.address = request.POST['address']
                candidate.city = request.POST['city']
                candidate.state = request.POST['state']
                if 'resume' in request.FILES:
                    candidate.resume = request.FILES['resume']
                candidate.save()
                return JsonResponse({'success': 'Candidate profile updated successfully'})
            else:
                return JsonResponse({'error': 'Please login to update candidate profile'})

        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred while updating candidate profile'})

    return JsonResponse({'error': 'An error occurred while updating candidate profile'})

def edit_company_profile(request, primary_key):
    company = Company.objects.get(id=primary_key)
    return render(request, 'editCompanyProfile.html', {'company': company})

def editCandidateProfile(request):
    return render(request, 'editCandidateProfile.html')

def edit_company_profile_attempt(request, primary_key):
    if request.method == 'POST':
        try:
            if request.session['is_signed_in']:
                company = Company.objects.get(id=primary_key)
                if 'profile' in request.FILES:
                    company.profile_pic = request.FILES['profile']
                company.company_name = request.POST['companyname']
                company.about = request.POST['about']
                company.contact = request.POST['contact']
                company.address = request.POST['address']
                company.city = request.POST['city']
                company.state = request.POST['state']
                company.website = request.POST['website']
                company.save()
                return JsonResponse({'success': 'Company profile updated successfully'})
            else:
                return JsonResponse({'error': 'Please login to update company profile'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred while updating company profile'})

    return JsonResponse({'error': 'An error occurred while updating company profile'})

def withdraw_application(request, primary_key):
    try:
        if request.session['is_signed_in']:
            candidate = Candidate.objects.get(id=request.session['id'])
            job = Job.objects.get(id=primary_key)
            application = JobApplication.objects.get(candidate=candidate, job=job)
            application.delete()
            job.number_of_applicants -= 1
            job.save()
            return redirect('candidateDashboard')
        else:
            return redirect('signIn')
    except Exception as e:
        print(e)
        return redirect('signIn')

def signOut(request):
    return render(request, 'signOut.html')

def sign_out_attempt(request):
    request.session.clear()
    return redirect('signIn')
