from api.views import * 
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('role/', RoleView),
    path('department/', DepartmentView),
    path('designation/', DesignationView ),
    path('customuser/', CustomUserView),
    path('employee/', EmployeeView),
    path('departmentpoc/', DepartmentPOCView),
    path('incidenttype/', Incident_typeView),
    path('contributingfactors/', Contributing_factorsView),
    path('incidentticket/', Incident_ticketView),
    path('send-email/', send_test_email),
    path('sent-otp/', email_otp),
    path('verify-otp/', verify_otp),
    path('request-reset/', request_reset_password),
    path('verify-reset/', otp_verification),
    path('reset-password/', reset_password),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', signout)
]