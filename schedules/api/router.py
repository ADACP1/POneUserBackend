from django.urls import path
from schedules.api.views import (ScheduleNotificationListView, ScheduleNotificationView,ScheduleDetailListView, ScheduleDetailView,ScheduleListView, ScheduleView,ScheduleCreateView, ScheduleUpdateView)

urlpatterns = [
    # ScheduleNotification endpoints
    path('schedule-notifications', ScheduleNotificationListView.as_view()),
    path('schedule-notifications/<int:pk>', ScheduleNotificationView.as_view()),

    # ScheduleDetail endpoints
    path('schedule-details', ScheduleDetailListView.as_view()),
    path('schedule-details/<int:pk>', ScheduleDetailView.as_view()),

    # Schedule endpoints
    path('schedules', ScheduleListView.as_view()),
    path('schedules/<int:pk>', ScheduleView.as_view()),
    path('schedules/create', ScheduleCreateView.as_view()),    
    path('schedules/update/<int:pk>', ScheduleUpdateView.as_view()),     
]
