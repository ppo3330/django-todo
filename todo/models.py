from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True) 

    def __str__(self):
        return self.title