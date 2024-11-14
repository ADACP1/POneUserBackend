from django.urls import path
from clocks.api.views import ClockCreateView,ClockListView,LastClockView,AbsenceTypeByCompanyListView,AbsenceTypeView,AbsenceTypeListView,AbsenceEmployeeListView,AbsenceEmployeeCreateView,AbsenceEmployeeValidateView
urlpatterns = [
    path('clocks',ClockListView.as_view()),
    path('clocks/create',ClockCreateView.as_view()),
    path('clocks/lastclock',LastClockView.as_view()),  
    path('absencetypes', AbsenceTypeListView.as_view()),
    path('absencetypes/<int:pk>', AbsenceTypeView.as_view()), 
    path('absencetypes/bycompany/<int:company_id>', AbsenceTypeByCompanyListView.as_view()),
    path('absenceemployee',AbsenceEmployeeListView.as_view()),
    path('absenceemployee/create',AbsenceEmployeeCreateView.as_view()),             
    path('absenceemployee/validate/<int:pk>',AbsenceEmployeeValidateView.as_view()),           
]