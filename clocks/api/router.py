from django.urls import path
from clocks.api.views import ClockCreateView,ClockListView,LastClockView
urlpatterns = [
    path('clocks',ClockListView.as_view()),
    path('clocks/create',ClockCreateView.as_view()),
    path('clocks/lastclock',LastClockView.as_view()),    
]