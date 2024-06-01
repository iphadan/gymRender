
from django.urls import path,include
from django.conf.urls.static import static
from gym import settings
from . import views
# from .views import ScannerView


urlpatterns = [
path('',views.loginUser,name='login'),
path('logout/',views.logoutUser,name='logout'),
path('home/',views.home,name='home'),
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





path('scanner/',views.scanner,name='scanner'),

path('qrScanner/<int:id>/', views.qrScanner,name='qrScanner'),
path('blockPlan/<int:id>/', views.blockPlan,name='blockPlan'),
path('unblockPlan/<int:id>/', views.unblockPlan,name='unblockPlan'),



path('send_message/', views.send_message,name='send_message'),






]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)