from django.urls import path

from app.views.authenticate import (UserLoginViewSet, UserLogoutViewSet,
                                    UserSignupViewSet)

urlpatterns = [
    path('', UserLoginViewSet.as_view(
        {'get': 'show_login', 'post': 'login_user'}), name='login'),
    path('signup/', UserSignupViewSet.as_view(
        {'get': 'show_signup', 'post': 'signup_user'}), name='signup'),
    path('logout/', UserLogoutViewSet.as_view(
        {'get': 'logout_user'}), name='logout')
]
