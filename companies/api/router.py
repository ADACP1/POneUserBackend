from django.urls import path
from companies.api.views import CompanyListView,CompanyView, UbicationView,UbicationListView,UbicationByCompanyListView
urlpatterns = [
    path('companies',CompanyListView.as_view()),
    path('companies/<int:pk>',CompanyView.as_view()),
    path('companies/ubications',UbicationListView.as_view()),    
    path('companies/<int:company_id>/ubications', UbicationByCompanyListView.as_view()),
    path('companies/<int:company_id>/ubications/<int:ubication_id>', UbicationView.as_view()),      
]