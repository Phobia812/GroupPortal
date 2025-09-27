from django.conf import settings
from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Grade(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField()
    detail = models.TextField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'subject', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.subject.name}: {self.grade} в {self.date}"
    
