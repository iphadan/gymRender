import base64
import datetime
from io import BytesIO
from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import now
import qrcode
from . import models
# import qrcode

# Create your views here.
def home(request):
    newGymMembers=models.GymMember.objects.filter(joinedAt=datetime.date.today())
    gymMembers=models.GymMember.objects.filter(joinedAt__year=datetime.date.today().year)
    thisMonthGymMembers=models.GymMember.objects.filter(joinedAt__month=datetime.date.today().month)
    print(thisMonthGymMembers)
    thisMonthRevenue=0
    for thisMonthGymMember in thisMonthGymMembers:
        if thisMonthGymMember.plan.price:
            thisMonthRevenue+=thisMonthGymMember.plan.price

    
   
    context={
        'newGymMembers':newGymMembers.__len__(),
        'gymMembers':gymMembers.__len__(),
        'thisMonthGymMembers':thisMonthGymMembers,
        'thisMonthRevenue':thisMonthRevenue

    }

    {

    }

    return render(request,'index.html',context)

def manageMembers(request):
    gymMembers=models.GymMember.objects.all()
    context={
        'gymMembers':gymMembers,
       

    }
    return render(request,'manageMembers.html',context)
def addNewMembers(request):
    return render(request,'registration.html')
def getIn(request):
    #if attendance in the day of getin is already taken , then count how many times the gym members come to the gym using noPerDay 
    if request.method == "POST":
        try:
            id=request.POST.get('gymMemberID')
            gymMember=models.GymMember.objects.get(pk=id)
            

        except:
            messages.error(request,"Gym Member with the provided ID does not exist, Please register the Customer")
            return render(request,'get_in.html')
        print(gymMember,datetime.date.today())
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


def plan(request):
    plans=models.Plan.objects.all()
    context={
        'plans':plans
    }
    return render(request,'plan.html',context)
def payment(request):
    return render(request,'payment.html')
def attendance(request):
    try:
        todayAttendance=models.Attendance.objects.filter(workoutDate=datetime.date.today())
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

def generate_qrcode(username, user_id):
    # Create the data string for the QR code
    data = f"Username: {username}, ID: {user_id}"

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
            qr_code_image = generate_qrcode(gymMember.firstName, gymMember.pk)
            
            context = {
            'qr_code_image': qr_code_image,
            'gymMember':gymMember
                }
            print(context)
            
            messages.success(request,"QR code Generation was Success")
            return render(request, 'generate_ID.html',context)
            
        except:
           print('except')
           messages.error(request,'Gym member with the provided ID does not exist')
           return render(request,'generate_ID.html')

    return render(request, 'generate_ID.html',{})
def reports(request):
    return render(request,'report.html')

