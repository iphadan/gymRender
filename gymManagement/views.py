import base64
import datetime
from io import BytesIO
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
import qrcode
from . import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
# import qrcode

# Create your views here.
def loginUser(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
            return render(request,'login.html')
    return render(request,'login.html')
def logoutUser(request):
    if request.user.is_authenticated :
        logout(request)
        messages.info(request,'Logged Out')
        return render(request,'login.html')
    else:
        return render(request,'login.html')
def home(request):
    if request.user.is_authenticated:
        newGymMembers=models.GymMember.objects.filter(joinedAt=datetime.date.today())
        gymMembers=models.GymMember.objects.filter(joinedAt__year=datetime.date.today().year)
        thisMonthGymMembers=models.GymMember.objects.filter(joinedAt__month=datetime.date.today().month).order_by('-paidAt')
        plans=models.Plan.objects.all()

        planRevenue={}
        for plan in plans:
            planRevenue[plan.name] = [models.GymMember.objects.filter(joinedAt=datetime.date.today(),plan=plan).count() * plan.price,models.Plan.objects.get(pk=plan.pk),models.GymMember.objects.filter(joinedAt=datetime.date.today(),plan=plan).count()]

        

        thisMonthRevenue=0
        for thisMonthGymMember in thisMonthGymMembers:
            if thisMonthGymMember.plan.price:
                thisMonthRevenue+=thisMonthGymMember.plan.price

        
    
        context={
            'newGymMembers':newGymMembers.__len__(),
            'gymMembers':gymMembers.__len__(),
            'thisMonthGymMembers':thisMonthGymMembers,
            'thisMonthRevenue':thisMonthRevenue,
            'planRevenue':planRevenue,
            'plans':plans,

        }

        {

        }
        print(request.user)

        return render(request,'index.html',context)
    messages.error(request,'login first')
    return render(request,'login.html')

def manageMembers(request):
    if request.user.is_authenticated:
        gymMembers=models.GymMember.objects.all().order_by('-paidAt')
        context={
            'gymMembers':gymMembers,
        

        }
        return render(request,'manageMembers.html',context)
    messages.error(request,'login first')
    return render(request,'login.html')

def addNewMembers(request):
    if request.user.is_authenticated:
        plans=models.Plan.objects.all()

        context={
            'plans':plans
        }
        if request.method == 'POST':
            firstName=request.POST.get('firstName')
            lastName=request.POST.get('lastName')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            photo=request.FILES.get('photo')
            plan=request.POST.get('plan')
            gender=request.POST.get('gender')
            
            
            try:
                plan=models.Plan.objects.get(pk=plan)
                expireDate= datetime.date.today() + relativedelta(days=plan.period)
                print(expireDate, '=>> + ',relativedelta(plan.period))
                # ,expireDate=datetime.date.today() + plan.period
                if photo:
                    gymMember=models.GymMember.objects.create(firstName=firstName,lastName=lastName,email=email,photo=photo,phone=phone,plan=plan,gender=gender,expireDate=expireDate)
                    print(gymMember.photo.url," ===> ",gymMember.photo)
                else:
                    gymMember=models.GymMember.objects.create(firstName=firstName,lastName=lastName,email=email,phone=phone,plan=plan,gender=gender)
            
                messages.success(request,'registered Successfully')
            except:
                messages.error(request,'Registration Failed, try again')

        return render(request,'registration.html',context)
    messages.error(request,'login first')
    return render(request,'login.html')

def updateMember(request,id):
    print(id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            firstName=request.POST.get('firstName')
            lastName=request.POST.get('lastName')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            photo=request.FILES.get('photo')
            # plan=request.POST.get('plan')
            gender=request.POST.get('gender')
            plan=models.Plan.objects.get(pk=plan)
            print(id,firstName,photo,str(plan.title),lastName,email,phone,gender)
            try:
                gymMember=models.GymMember.objects.filter(id=id)

                # ,expireDate=datetime.date.today() + plan.period
                if photo:
                    print(photo)
                    gymMember.update(firstName=firstName,lastName=lastName,email=email,photo=photo,phone=phone,gender=gender)
                else:
                    gymMember.update(firstName=firstName,lastName=lastName,email=email,phone=phone,gender=gender)
                    
                    
                messages.success(request,f'Gym Member with {gymMember.pk} ID Updated Successfully')
                return redirect('manageMembers')
                
            except:
                gymMember=models.GymMember.objects.get(id=id)
                plans=models.Plan.objects.all()
                context={
                'plans':plans
                ,'gymMember':gymMember
                  }
                messages.error(request,'Update Failed, try again')
                return render(request,f'update_user.html',context)
        try:
            gymMember=models.GymMember.objects.get(id=id)
            plans=models.Plan.objects.all()
            context={
                'plans':plans
                ,'gymMember':gymMember
                  }
        except:
             
                messages.error(request,'Something went wrong')
                return redirect('manageMembers')
    
        return render(request,'update_user.html',context)
    messages.error(request,'login first')
    return render(request,'login.html')


def updatePlan(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            planTitle=request.POST.get('planTitle')
            planName=request.POST.get('planName')
            period=request.POST.get('period')
            price=request.POST.get('price')
            print(planName,planTitle,period,price)

            try:
                newPlan=models.Plan.objects.filter(id=id).update(name=planName,title=planTitle,period=period,price=price)
                messages.success(request,'Plan Updated Successfully')
                return redirect('plan')
            except Exception:
                print(Exception)
                messages.error(request,'Something went wrong, try agian later')
        
            
        try:
            plan=models.Plan.objects.get(pk=id)
        except:
            messages.error(request,'Gym Member with the provieded ID does not exist !')
            return render(request,'updatePlan.html')
        context={ 'plan':plan}
        
        
        return render(request,'updatePlan.html',context)
        
    messages.error(request,'login first')
    return render(request,'login.html')

def gymMemberProfile(request,id):
        if request.user.is_authenticated:
            try:
                gymMember=models.GymMember.objects.get(pk=id)
                
                context={
                        'gymMember':gymMember,
                        'today':datetime.datetime.today()
                    }

            except:
                messages.error(request,f'Gym Member with the provided {gymMember.pk} ID does not exist! ')
                context={}
            
            return render(request,'gymMemberProfile.html',context)
        messages.error(request,'login first')
        return render(request,'login.html')    






def getIn(request):
    if request.user.is_authenticated:
        #if attendance in the day of getin is already taken , then count how many times the gym members come to the gym using noPerDay 
        if request.method == "POST":
            try:
                id=request.POST.get('gymMemberID')
                gymMember=models.GymMember.objects.get(pk=id)
                if gymMember.expireDate > datetime.date.today():
                    ...
                else:
                    messages.error(request,"Expired ID  Please, Pay First ") 
                    return render(request,'get_in.html')
                

            except:
                messages.error(request,f"Gym Member with the provided {gymMember.pk} ID does not exist, Please register the Customer")
                return render(request,'get_in.html')
        
            workoutDate=datetime.date.today()
                
            try:
                todayAttendance=models.Attendance.objects.filter(workoutDate=datetime.date.today())
                print(todayAttendance[-1].noPerDay)
                todayAttendance[-1].noPerDay=todayAttendance[-1].noPerDay+1
                todayAttendance[-1].save()
                messages.success(request,'Attendance Successfully Taken Again')
            except:
                try:
                    attendance=models.Attendance.objects.create(gymMember=gymMember)
                    attendance.noPerDay+=1
                    attendance.save()
                    messages.success(request,'Attendance Successfully Taken')
                except:
                    messages.error(request,'Something went wrong, try again ')

        return render(request,'get_in.html')
    messages.error(request,'login first')
    return render(request,'login.html')


def registerPlan(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            planTitle=request.POST.get('planTitle')
            planName=request.POST.get('planName')
            period=request.POST.get('period')
            price=request.POST.get('price')
            print(planName,planTitle,period,price)

            try:
                newPlan=models.Plan.objects.create(name=planName,title=planTitle,period=period,price=price)
                messages.success(request,'New Plan Added Successfully')
            except:
                messages.error(request,'Somethin went error, try agian later')
        return render(request,'add_new_plan.html')
    messages.error(request,'login first')
    return render(request,'login.html')

def plan(request):
    if request.user.is_authenticated:
        plans=models.Plan.objects.all().order_by('-createdAt')
        context={
            'plans':plans
        }
        return render(request,'plan.html',context)
    messages.error(request,'login first')
    return render(request,'login.html')
def payment(request):
        if request.user.is_authenticated:
            try:
                plans=models.Plan.objects.all()
            except:

                messages.error(request,'There is No Plan/Package Registered yet')
                return redirect('home')
            context={
                'plans':plans
            }
            if request.method == 'POST':
                try:
                
                    gymMember=models.GymMember.objects.filter(id=request.POST.get('id'))
                    plan=models.Plan.objects.get(pk=request.POST.get('plan'))
            
                    if gymMember[0].expireDate < datetime.date.today():
                        expireDate = gymMember[0].expireDate + relativedelta(days=plan.period)
                    else:
                        expireDate = datetime.date.today() + relativedelta(days=plan.period)
                    print(expireDate)
                    gymMember.update(expireDate = expireDate)
                    print(gymMember[0].expireDate)
                    messages.info(request,'Expire Date updated')
                except :
                        messages.error(request,'something went wrong, try again later')
                        return render(request,'payment.html',context)


                                    
        
        return render(request,'payment.html',context)
def attendance(request):
    if request.user.is_authenticated:    
        try:
            todayAttendance=models.Attendance.objects.filter(workoutDate=datetime.date.today()).order_by('-workoutTime')
            print(todayAttendance)
            context={
                'todayAttendance':todayAttendance
            }
        except:
            messages.error(request,'No attendance takey yet')
            context={
                'attendance':[]
            }
        return render(request,'attendance.html',context)
    messages.error(request,'login first')
    return render(request,'login.html')


def generate_qrcode(gymMember,expired):
    # Create the data string for the QR code
        
        
    data = f"Full Name: {gymMember.firstName +' ' + gymMember.lastName},\n ID: # {gymMember.pk} \n Join Date : {gymMember.joinedAt}  \n Expire Date : {gymMember.expireDate} \n Status: {expired}"

    # Generate the QR code image
    qr_code = qrcode.make(data)

    # Create a BytesIO object to store the image data
    buffer = BytesIO()

    # Save the QR code image to the BytesIO object in PNG format
    qr_code.save(buffer, format='PNG')

    # Set the file pointer to the beginning of the BytesIO object
    buffer.seek(0)

    # Convert the image data to base64-encoded string
    image_data = base64.b64encode(buffer.getvalue()).decode()

    return image_data

def generateIdCard(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                id=request.POST.get('id')
                gymMember=models.GymMember.objects.get(pk=id)
                expired=""
                if gymMember.expireDate > datetime.date.today():
                    expired= "Not Expired"
                else:
                    expired= "Expired"
                qr_code_image = generate_qrcode(gymMember,expired)
                
                context = {
                'qr_code_image': qr_code_image,
                'gymMember':gymMember,
                'expired':expired
                
                }
            
                return render(request, 'generate_ID.html',context=context)
                
            except:
            
                messages.error(request,'Gym member with the provided ID does not exist')
                return render(request,'generate_ID.html')

        return render(request, 'generate_ID.html',{})
    messages.error(request,'login first')
    return render(request,'login.html')

def reports(request):
    if request.user.is_authenticated:
        gymMembersList=models.GymMember.objects.all()
        gymMembers={}
        for gymMember in  gymMembersList:
            if gymMember.expireDate < datetime.date.today():
                gymMembers[gymMember] = [True,0]
            else:
                gymMembers[gymMember] = [False,gymMember.expireDate - datetime.date.today()]

        
        context={
            'gymMembers':gymMembers,
        }
        return render(request,'report.html',context)
    messages.error(request,'login first')
    return render(request,'login.html')
def scanner(request):
    return render(request,'scanner.html')

@api_view(['GET'])
def qrScanner(request, id):
    try:
        gym_member = models.GymMember.objects.get(pk=id)
        context = {
            'gymMember': gym_member
        }
        return render(request, 'rest_framework/api.html', context)
    except models.GymMember.DoesNotExist:
        return Response({'error': f'Gym member with ID {id} not found.'}, status=404)