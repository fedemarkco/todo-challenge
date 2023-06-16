from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(blank=False, null=True)
    completed = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self):
        return self.title
