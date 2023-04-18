from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from .forms import *
from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.db.models import Sum



def home(request):
    if request.user.is_authenticated:
        candidates=Candidates.objects.filter(company__name=request.user.username)
        context={
            'candidates':candidates,
        }
        return render(request,'hr.html',context)
    else:
        companies=Company.objects.all()
        context={
            'companies':companies,
        }
        return render(request,'Jobseeker.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('home')
       return render(request,'login.html')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        Form=UserCreationForm()
        register_form = RegisterForm()
        if request.method=='POST':
            Form=UserCreationForm(request.POST)
            register_form = RegisterForm(request.POST)
            if Form.is_valid() and register_form.is_valid():
                currUser=Form.save()
                registerData = register_form.save(commit=False)
                Company.objects.create(user=currUser,name=currUser.username, position=registerData.position, description=registerData.description, salary=registerData.salary,
                                       experience=registerData.experience, Location=registerData.Location)
                return redirect('login')
        context={
            'form':Form,
            'registerForm': register_form
        }
        return render(request,'register.html',context)

def applyPage(request):
    form=ApplyForm()
    if request.method=='POST':
        form=ApplyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'apply.html',context)

def plotData(request):
    companies = Company.objects.all()
    name_values = companies.values_list('name', flat=True)
    name_list = list(name_values)
    countList = []
    for company in name_list:
        count = Candidates.objects.filter(company__name = company).count()
        countList.append(count)
    print(name_list,countList)
    fig = Figure()
    ax = fig.add_subplot()
    
    ax.pie(countList, labels=name_list, autopct='%1.1f%%')
    

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode('utf-8')

    # Pass the base64-encoded image to the template context
    context = {'image': image_base64}
    return render(request, 'plot.html', context)

def plotDataBar(request):
    companies = Company.objects.all()
    company_list = []
    salary_list = []
   
    for company in companies:
        candidates = Candidates.objects.filter(company=company)
        total_salary = Company.objects.aggregate(Sum('salary'))['salary__sum'] or 0

        company_list.append(company.name)
        salary_list.append(total_salary)
    
    print(company_list, salary_list)
    fig = Figure()
    ax = fig.add_subplot()
    
    ax.bar(company_list, salary_list)
    ax.set_xlabel('Company', fontsize=10)
    ax.set_ylabel('Total Salary', fontsize=10)
    ax.set_title('Total Salary by Company', fontsize=16)
    ax.set_xticklabels(company_list, rotation=20, ha='right')


    
    

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png).decode('utf-8')

    # Pass the base64-encoded image to the template context
    context = {'image': image_base64}
    return render(request, 'plot.html', context)
    