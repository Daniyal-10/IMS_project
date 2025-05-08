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
    path('incidentticket/', Incident_ticketView)
]