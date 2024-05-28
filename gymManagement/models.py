import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
# class gymAdmin(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)

class Plan(models.Model):
    name=models.CharField(max_length=50,default='normal')
    title=models.CharField(max_length=50)
    period=models.IntegerField(default=30)
    price=models.IntegerField(default=0)

    createdAt=models.DateTimeField(default=datetime.datetime.today())


    def __str__(self) -> str:
        return self.title + " " + str(self.price)

class GymMember(models.Model):
    firstName=models.CharField(max_length=50)
    lastName=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=14,default='0900000000')
    gender=models.CharField(max_length=8,default="Male")
    photo=models.ImageField(upload_to='upload/profile',blank=True,null=True,default='upload/profile/defaultUserImg.jpeg')
    plan=models.ForeignKey(Plan,on_delete=models.SET_NULL,null=True,blank=True)
    expireDate=models.DateField(default=datetime.date.today())
    joinedAt=models.DateField(default=datetime.date.today())
    paidAt=models.DateTimeField(default=datetime.datetime.today())
    active=models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.firstName + " " + self.lastName
class Attendance(models.Model):
    gymMember=models.ForeignKey(GymMember,on_delete=models.CASCADE)
    workoutTime=models.TimeField(default=datetime.datetime.now())
    workoutDate=models.DateField(default=datetime.date.today())
    noPerDay=models.IntegerField(default=0)




    
