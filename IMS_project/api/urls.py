from api.views import * 
from django.urls import path


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

]