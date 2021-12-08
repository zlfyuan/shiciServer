from django.urls import path, include
from user.views import UserInfoView, FeedBackView

urlpatterns = [
    path('api/user/info/', UserInfoView.as_view()),
    path('api/user/feedback/', FeedBackView.as_view()),
]
