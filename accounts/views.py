from accounts.forms import UserForm, TraineeForm, CompanyForm, EducationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Education, Trainee, User
from django.contrib.auth.decorators import login_required
from django import forms

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        trainee_form = TraineeForm(data=request.POST)
        if user_form.is_valid() and trainee_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            trainee = trainee_form.save(commit=False)
            trainee.user = user
            trainee.cv = request.FILES['cv']
            trainee.save()
            registered = True
            return redirect('/accounts/login/')
        else:
            print (user_form.errors, trainee_form.errors)
    else:
        user_form = UserForm()
        trainee_form = TraineeForm()
    return render(request,
            'accounts/register.html',
            {'user_form': user_form, 'trainee_form': trainee_form, 'registered': registered} )


def registerCompany(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        company_form = CompanyForm(data=request.POST)
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            company = company_form.save(commit=False)
            company.user = user
            company.save()
            registered = True
            return redirect('/accounts/login/')
        else:
            print (user_form.errors, company_form.errors)
    else:
        user_form = UserForm()
        company_form = CompanyForm()
        return render(request,
            'accounts/registerCompany.html',
            {'user_form': user_form, 'company_form': company_form, 'registered': registered} )



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/accounts/create/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'accounts/login.html', {})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/accounts/login')



@login_required(login_url="/accounts/login/")
def create_education(request):
    educations = Education.objects.filter(trainee=request.user)
    user = request.user
    trainees = Trainee.objects.all()
    if request.method == 'POST':
        form = EducationForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.trainee = request.user
            instance.save()
            return redirect('/accounts/create')
    else:
        form = EducationForm()
    return render(request, 'accounts/create.html', {'form':form, 'educations':educations, 'user':user, 'trainees':trainees})

def edit(request, id):
    educations = Education.objects.get(id=id)
    context = {'educations': educations}
    return render(request, 'accounts/edit.html', context)

def editTrainee(request, id):
    trainee = Trainee.objects.get(id=id)
    user = trainee.user
    context = {'trainee': trainee, 'user':user}
    return render(request, 'accounts/editTrainee.html', context)

def update(request, id):
    education = Education.objects.get(id=id)
    education.school_name = request.POST['school_name']
    education.diploma = request.POST['diploma']
    education.start_date = request.POST['start_date']
    education.end_date = request.POST['end_date']
    education.save()
    return redirect('/accounts/create')

def updateTrainee(request, id):
    trainee = Trainee.objects.get(id=id)
    user = trainee.user
    trainee.first_name = request.POST['first_name']
    trainee.last_name = request.POST['last_name']
    trainee.date_of_birth = request.POST['date_of_birth']
    user.phone = request.POST['phone']
    user.email = request.POST['email']
    user.address = request.POST['address']
    trainee.save()
    user.save()
    return redirect('/accounts/create')

def delete(request, id):
    education = Education.objects.get(id=id)
    education.delete()
    return redirect('/accounts/create')


#def index(request):
#    members = Member.objects.all()
#    context = {'members': members}
#    return render(request, 'crud/index.html', context)
