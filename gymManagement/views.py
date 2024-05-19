import base64
import datetime
from io import BytesIO
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.timezone import now
import qrcode
from . import models
# import qrcode

# Create your views here.
def home(request):
    newGymMembers=models.GymMember.objects.filter(joinedAt=datetime.date.today())
    gymMembers=models.GymMember.objects.filter(joinedAt__year=datetime.date.today().year)
    thisMonthGymMembers=models.GymMember.objects.filter(joinedAt__month=datetime.date.today().month).order_by('-paidAt')
    plans=models.Plan.objects.all()

    planRevenue={}
    for plan in plans:
        planRevenue[plan.name] = [models.GymMember.objects.filter(joinedAt=datetime.date.today(),plan=plan).count() * plan.price,models.Plan.objects.get(pk=plan.pk),models.GymMember.objects.filter(joinedAt=datetime.date.today(),plan=plan).count()]

    
    print(planRevenue)

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

    return render(request,'index.html',context)

def manageMembers(request):
    gymMembers=models.GymMember.objects.all().order_by('-paidAt')
    context={
        'gymMembers':gymMembers,
       

    }
    return render(request,'manageMembers.html',context)
def addNewMembers(request):
    
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
        plan=models.Plan.objects.get(pk=plan)
        print(firstName,photo,str(plan.title),lastName,email,phone,gender)
        try:
            # ,expireDate=datetime.date.today() + plan.period
            if photo:
                gymMember=models.GymMember.objects.create(firstName=firstName,lastName=lastName,email=email,photo=photo,phone=phone,plan=plan,gender=gender)
                print(gymMember.photo.url," ===> ",gymMember.photo)
            else:
                gymMember=models.GymMember.objects.create(firstName=firstName,lastName=lastName,email=email,phone=phone,plan=plan,gender=gender)
        
            messages.success(request,'registered Successfully')
        except:
            messages.error(request,'Registration Failed, try again')

    return render(request,'registration.html',context)
def updateMember(request,id):
    if request.method == 'POST':
       
        firstName=request.POST.get('firstName')
        lastName=request.POST.get('lastName')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        photo=request.FILES.get('photo')
        plan=request.POST.get('plan')
        gender=request.POST.get('gender')
        plan=models.Plan.objects.get(pk=plan)
        print(firstName,photo,str(plan.title),lastName,email,phone,gender)
        try:
            # ,expireDate=datetime.date.today() + plan.period
            if photo:
                gymMember=models.GymMember.objects.update(pk=id,firstName=firstName,lastName=lastName,email=email,photo=photo,phone=phone,plan=plan,gender=gender)
                print(gymMember.photo.url," ===> ",gymMember.photo)
            else:
                gymMember=models.GymMember.objects.update(pk=id,firstName=firstName,lastName=lastName,email=email,phone=phone,plan=plan,gender=gender)
        
            messages.success(request,'registered Successfully')
            return redirect(request,'manageMembers')
            
        except:
            messages.error(request,'Registration Failed, try again')
            return render(request,'update_user.html')
            
    else:

        gymMember=models.GymMember.objects.get(pk=id)
        plans=models.Plan.objects.all()
        context={
            'plans':plans
            ,'gymMember':gymMember
        }

    return render(request,'update_user.html',context)

def updatePlan(request,id):
    try:
        plan=models.Plan.objects.get(pk=id)
    except:
        messages.error(request,'Gym Member with the provieded ID does not exist !')
        return render(request,'updatePlan.html')
    context={ 'plan':plan}
       
    
    print('updateplan')
    return render(request,'updatePlan.html',context)

def gymMemberProfile(request,id):
    try:
        gymMember=models.GymMember.objects.get(pk=id)
        
        context={
                'gymMember':gymMember,
                'today':datetime.datetime.today()
            }

    except:
        messages.error(request,'Gym Member with the provided ID does not exist! ')
        context={}
    
    return render(request,'gymMemberProfile.html',context)





def getIn(request):
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
            messages.error(request,"Gym Member with the provided ID does not exist, Please register the Customer")
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

def registerPlan(request):
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
def plan(request):
    plans=models.Plan.objects.all().order_by('-createdAt')
    context={
        'plans':plans
    }
    return render(request,'plan.html',context)
def payment(request):
    return render(request,'payment.html')
def attendance(request):
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

def generate_qrcode(gymMember,expired):
    # Create the data string for the QR code
        
        
    data = f"Full Name: {gymMember.firstName +' ' + gymMember.lastName},\n ID: # {gymMember.pk} \n Expire Date : {gymMember.expireDate} \n Expire ?:{expired}"

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
            print(context)
            return render(request, 'generate_ID.html',context=context)
            
        except:
           print('except')
           messages.error(request,'Gym member with the provided ID does not exist')
           return render(request,'generate_ID.html')

    return render(request, 'generate_ID.html',{})
def reports(request):
    gymMembersList=models.GymMember.objects.all()
    gymMembers={}
    for gymMember in  gymMembersList:
        if gymMember.expireDate < datetime.date.today():
            gymMembers[gymMember] = True
        else:
            gymMembers[gymMember] = False

    
    context={
        'gymMembers':gymMembers,
    }
    return render(request,'report.html',context)