from django.urls import path
from login import views

urlpatterns = [
    path("api/register/", views.RegisterView.as_view()),
    path("api/login/", views.LoginView.as_view()),
    path("api/send/email/", views.SendEmailCodeView.as_view()),
    path('api/forget/password/', views.ForgetPasswordView.as_view()),
    path('api/change/password/', views.ChangePasswordView.as_view()),
    path('api/weixin/loginsession/', views.WeixinLogin.as_view()),
    # url(r'^api/login/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # url(r'^api/login/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
