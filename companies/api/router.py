from django.urls import path
from companies.api.views import CompanyListView,CompanyView, UbicationView,UbicationListView
urlpatterns = [
    path('companies',CompanyListView.as_view()),
    path('companies/<int:pk>',CompanyView.as_view()),
    path('companies/<int:company_id>/ubications/', UbicationListView.as_view()),
    path('companies/<int:company_id>/ubications/<int:ubication_id>/', UbicationView.as_view()),      
]