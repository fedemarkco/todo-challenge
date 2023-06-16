import logging

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers import UserLoginSerializers, UserSignupSerializers
from ..utils import MyHTMLRenderer

logger = logging.getLogger(__name__)


class UserLoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializers
    renderer_classes = [MyHTMLRenderer]
    template_name = 'login.html'

    def show_login(self, request):
        """
        Shows the template for the login.
        If the user is authenticated, it redirects
        them to create a new task
        """
        if request.user.is_authenticated:
            return redirect('new-task')
        serializer = UserLoginSerializers()
        return Response({'serializer': serializer})

    def login_user(self, request):
        """
        Creates the login for the user and redirects
        them to create a new task
        """
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            logger.debug(f'User {user} logged in.')
            login(request, user)
            return redirect('new-task')
        if 'Incorrect Credentials Passed.' in str(serializer._errors):
            return Response(
                {'serializer': serializer, 'error': 'Datos incorrectos!'})
        return Response({'serializer': serializer})


class UserSignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializers
    renderer_classes = [MyHTMLRenderer]
    template_name = 'signup.html'

    def show_signup(self, request):
        """
        Shows the template for the signup.
        If the user is authenticated, it redirects
        them to create a new task
        """
        if request.user.is_authenticated:
            return redirect('new-task')
        serializer = UserSignupSerializers()
        return Response({'serializer': serializer})

    def signup_user(self, request):
        """
        Creates a new account for the user and redirects
        them to create a new task
        """
        serializer = UserSignupSerializers(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.debug(f'User {user} created an account.')
            login(request, user)
            return redirect('new-task')
        if 'User exist!' in str(serializer._errors):
            return Response(
                {'serializer': serializer, 'error': 'El usuario no existe!'})
        return Response({'serializer': serializer})


class UserLogoutViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializers

    def logout_user(self, request):
        """
        If the user is authenticated, it logout and
        redirects him to the login
        """
        if request.user.is_authenticated:
            logger.debug(f'User {request.user} logged off.')
            logout(request)
        return redirect('/')
