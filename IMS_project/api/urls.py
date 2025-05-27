from api.views import * 
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'employeeview', EmployeeViewSet)
router.register(r'incidentview', IncidentViewSet)

urlpatterns = [
    path('role/', RoleView),
    path('department/', DepartmentView),
    path('designation/', DesignationView ),
    path('customuser/', CustomUserView),
    path('employee/', EmployeeView),
    path('departmentpoc/', DepartmentPOCView),
    path('incidenttype/', Incident_typeView),
    path('contributingfactors/', Contributing_factorsView),
    path('stakeholder/', stake_holderView),
    path('incidentticket/', Incident_ticketView),
    path('incidentticket2/', IncidentTicketDetails),
    path('filterticket/<int:requestor_id>/', FilterTicket),
    path('send-email/', send_test_email),
    path('sent-otp/', email_otp),
    path('verify-otp/', verify_otp),
    path('request-reset/', request_reset_password),
    path('verify-reset/', otp_verification),
    path('reset-password/', reset_password),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('  ', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', signout),
    path("emp1/", employee_v),
    path("emp2/", employee_v2),
    #********************ModelVIewSet****************
    path('',include(router.urls)),
]   