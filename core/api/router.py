from django.urls import path
from core.api.views import CountryListView,CountryView,LanguageListView,LanguageView, CityListView,CityView
urlpatterns = [
    path('countries',CountryListView.as_view()),
    path('countries/<int:pk>',CountryView.as_view()),
    path('cities/all/<int:country>',CityListView.as_view()),
    path('cities/<int:pk>',CityView.as_view()),    
    path('languages',LanguageListView.as_view()),
    path('languages/<int:pk>',LanguageView.as_view()),    
]