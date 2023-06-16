from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='marco@gmail.com',
            password='1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_task_status_code_200(self):
        """
        Call the new-task url and return a status code 200
        """
        url = reverse('new-task')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        """
        Create a new task and add it to the Task model
        """
        url = reverse('new-task')
        data = {
            'title': "Título",
            'description': "Description",
            'completed': False
        }
        response = self.client.post(url, data=data)
        self.assertTrue(
            'Tarea agregada correctamente!' in response.content.decode()
        )
        task = Task.objects.all()
        self.assertEqual(len(task), 1)

    def test_all_tasks_status_code(self):
        """
        Call the all-task url and return a status code 200
        """
        url = reverse('all-tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_tasks_get_task(self):
        """
        Get all tasks of the Task model
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False
        )
        url = reverse('all-tasks')
        response = self.client.get(url)
        self.assertTrue('Título' in response.content.decode())
        self.assertTrue('Description' in response.content.decode())

    def test_set_completed_task_status_code(self):
        """
        Call the set-completed-task url and return a status code 200
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False
        )
        url = reverse('set-completed-task', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_completed_post(self):
        """
        Sets a task as completed and redirects it to all-tasks url
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False
        )
        url = reverse('set-completed-task', kwargs={'pk': 1})
        response = self.client.post(url)
        self.assertEqual('/task/all-tasks/', response.url)

    def test_delete_task_status_code(self):
        """
        Call the delete-task url and return a status code 200
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False
        )
        url = reverse('delete-task', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task_post(self):
        """
        Delete a task and redirect it to all-tasks url
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False
        )
        url = reverse('set-completed-task', kwargs={'pk': 1})
        response = self.client.post(url)
        self.assertEqual('/task/all-tasks/', response.url)

    def test_search_tasks_status_code(self):
        """
        Call the search-tasks url and return a status code 200
        """
        url = reverse('search-tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_tasks_by_date(self):
        """
        Gets all the tasks that match the searched date
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False,
            created_date='15/06/2023'
        )
        url = reverse('search-tasks')
        response = self.client.post(
            url,
            data={'search_title': '', 'search_date': '2023-06-15'}
        )
        self.assertTrue('Título' in response.content.decode())
        self.assertTrue('Description' in response.content.decode())

    def test_search_tasks_by_text(self):
        """
        Gets all tasks that match the search text
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False,
            created_date='15/06/2023'
        )
        url = reverse('search-tasks')
        response = self.client.post(
            url,
            data={'search_title': 'Description', 'search_date': ''}
        )
        self.assertTrue('Título' in response.content.decode())
        self.assertTrue('Description' in response.content.decode())

    def test_search_tasks_by_text_date(self):
        """
        Gets all tasks that match the text and date searched
        """
        Task.objects.create(
            user=self.user,
            title="Título",
            description="Description",
            completed=False,
            created_date='15/06/2023'
        )
        url = reverse('search-tasks')
        response = self.client.post(
            url,
            data={'search_title': 'Description', 'search_date': '2023-06-15'}
        )
        self.assertTrue('Título' in response.content.decode())
        self.assertTrue('Description' in response.content.decode())
