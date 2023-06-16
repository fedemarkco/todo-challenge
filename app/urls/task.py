from django.urls import path

from app.views.task import TaskViewSet

urlpatterns = [
    path('new-task/', TaskViewSet.as_view(
        {'get': 'new_task', 'post': 'create_task'}), name='new-task'),
    path('all-tasks/', TaskViewSet.as_view(
        {'get': 'all_tasks'}), name='all-tasks'),
    path('search-tasks/', TaskViewSet.as_view(
        {'get': 'search_tasks', 'post': 'search_tasks'}), name='search-tasks'),
    path('delete-task/<int:pk>', TaskViewSet.as_view(
        {'get': 'delete_task', 'post': 'delete_task'}), name='delete-task'),
    path('set-completed-task/<int:pk>', TaskViewSet.as_view(
        {'get': 'set_completed_task', 'post': 'set_completed_task'}),
        name='set-completed-task')
]
