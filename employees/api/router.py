from django.urls import path
from employees.api.views import ManagerListView,ManagerView,ManagerCompanyListView,ManagerCompanyListLiteView,AddCompanyToManagerView,RemoveCompanyFromManagerView,DepartmentListView,DepartmentView,PositionListView,PositionView, DownloadDepartmentTemplateView,DownloadEmployeeTemplateView,DownloadPositionTemplateView,UploadDepartmentFileView,UploadEmployeeFileView,UploadPositionFileView
urlpatterns = [
    path('managers', ManagerListView.as_view()),
    path('managers/<int:pk>', ManagerView.as_view()),
    path('managers/companies', ManagerCompanyListView.as_view()),
    path('managers/companies/lite', ManagerCompanyListLiteView.as_view()),    
    path('managers/<int:pk>/addcompany/<int:company_id>', AddCompanyToManagerView.as_view()),
    path('managers/<int:pk>/removecompany/<int:company_id>', RemoveCompanyFromManagerView.as_view()),
    path('departments', DepartmentListView.as_view()),
    path('departments/<int:pk>', DepartmentView.as_view()),    
    path('positions', PositionListView.as_view()),
    path('positions/<int:pk>', PositionView.as_view()),
    path('employees/download-employee-template/', DownloadEmployeeTemplateView.as_view()),            
    path('department/download-department-template/', DownloadDepartmentTemplateView.as_view()),                
    path('position/download-position-template/', DownloadPositionTemplateView.as_view()),                
    path('employees/upload-employee-template/', UploadEmployeeFileView.as_view()),            
    path('department/upload-department-template/', UploadDepartmentFileView.as_view()),                
    path('position/upload-position-template/', UploadPositionFileView.as_view()),       
]