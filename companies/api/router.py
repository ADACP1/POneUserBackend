from django.urls import path
from companies.api.views import CompanyListView,CompanyView
urlpatterns = [
    path('companies',CompanyListView.as_view()),
    path('companies/<int:pk>',CompanyView.as_view()),
]