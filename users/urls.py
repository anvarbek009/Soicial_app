from django.urls import path
from .views import UserCreateView, VerifyAPIView, GetNewVerification, ChangeUserInformationView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('new-verify-code/', GetNewVerification.as_view(), name='get-new-verify-code'),
    path('change-user-info/', ChangeUserInformationView.as_view(), name='change-user-info'),
]
