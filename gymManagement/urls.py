
from django.urls import path,include
from . import views
# from .views import ScannerView


urlpatterns = [
path('',views.home,name='home'),
path('manageMembers/',views.manageMembers,name='manageMembers'),
path('addNewMember/',views.addNewMembers,name='addNewMember'),
path('updateMember/<int:id>',views.updateMember,name='updateMember'),
path('gymMemberProfile/<int:id>',views.gymMemberProfile,name='gymMemberProfile'),

path('updatePlan/<int:id>',views.updatePlan,name='updatePlan'),

path('getIn/',views.getIn,name='getIn'),

path('plan/',views.plan,name='plan'),
path('registerPlan/',views.registerPlan,name='registerPlan'),
path('payment/',views.payment,name='payment'),
path('attendance/',views.attendance,name='attendance'),
path('generateIdCard/',views.generateIdCard,name='generateIdCard'),
path('reports/',views.reports,name='reports'),
path('qr_code/', include('qr_code.urls', namespace="qr_code")),

path('login/',views.loginUser,name='login'),
path('logout/',views.logoutUser,name='logout'),


<<<<<<< HEAD
path('scanner/',views.scanner,name='scanner'),

path('qrScanner/<int:id>/', views.qrScanner,name='qrScanner'),
=======
# path('scanner1/',views.scanner1,name='scanner1'),
# path('scanner/<int:id>',views.scanner,name='scanner'),

# path('api/scanner/<int:id>/', ScannerView.as_view(), name='scanner-api'),

>>>>>>> 04e88cf79a3604bc2093ccbf3abe3865c9a4bfe7






]