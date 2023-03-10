from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    """
    Модель записи заметки
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes', related_query_name='note')
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.title} от пользователя {self.user}'