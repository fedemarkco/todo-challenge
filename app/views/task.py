import logging

from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Task
from ..serializers import TaskSerializers
from ..utils import MyHTMLRenderer

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    renderer_classes = [MyHTMLRenderer]
    permission_classes = (IsAuthenticated,)

    def new_task(self, request):
        """
        Show the template to create the new task
        """
        serializer = TaskSerializers()
        return Response({'serializer': serializer},
                        template_name='new_task.html')

    def all_tasks(self, request):
        """
        Shows the template to list all tasks created by the user
        """
        queryset = Task.objects.filter(user=request.user).order_by('-id')
        return Response({'items': queryset},
                        template_name='list_task.html')

    def delete_task(self, request, pk):
        """
        If it is a GET method, it shows the template to delete the task
        If it is a POST method, it delete the task
        """
        if request.method == 'GET':
            query = Task.objects.get(id=pk)
            return Response({'item': query},
                            template_name='delete_task.html')
        if request.method == 'POST':
            query = Task.objects.get(id=pk)
            query.delete()
            logger.debug(
                f'User {self.request.user} deleted task: {query.title}.')
            return redirect('all-tasks')

    def set_completed_task(self, request, pk):
        """
        If it is a GET method, it shows the template to set a task
        as completed
        If it is a POST method, set the task as completed
        """
        if request.method == 'GET':
            query = Task.objects.get(id=pk)
            return Response({'item': query},
                            template_name='set_completed_task.html')
        if request.method == 'POST':
            query = Task.objects.get(id=pk)
            query.completed = True
            query.save()
            logger.debug(
                f'User {self.request.user} set completed task: {query.title}.')
            return redirect('all-tasks')

    def create_task(self, request):
        """
        Create the new task
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            title = request.data["title"]
            logger.debug(
                f'User {self.request.user} created new task: {title}.')
            return Response({'added': True},
                            template_name='new_task.html')
        return Response({'serializer': serializer},
                        template_name='new_task.html')

    def search_tasks(self, request):
        """
        If it is a GET method, it shows the template to search task
        If it is a POST method, search for user tasks, by date,
        by task content, or both and return a list of tasks
        """
        if request.method == 'GET':
            return Response(template_name='search_task.html')
        if request.method == 'POST':
            text = request.data["search_title"]
            date = request.data["search_date"]
            if text and date:
                queryset = Task.objects.filter(
                    Q(user=request.user) &
                    ((Q(title__contains=text) | Q(description__contains=text))
                     & Q(created_date=date))
                ).order_by('-id')
            elif text:
                queryset = Task.objects.filter(
                    Q(user=request.user) &
                    (Q(title__contains=text) | Q(description__contains=text))
                ).order_by('-id')
            elif date:
                queryset = Task.objects.filter(
                    user=request.user, created_date=date).order_by('-id')
            else:
                queryset = Task.objects.filter(user=request.user)

            return Response({'items': queryset},
                            template_name='list_task.html')
