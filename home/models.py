from django.db import models

class GroupInfo(models.Model):
    group_name = models.CharField(max_length=100, verbose_name="Назва групи")
    curator = models.CharField(max_length=200, verbose_name="Куратор")
    student_count = models.PositiveIntegerField(verbose_name="Кількість студентів")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Інформація про групу"
        verbose_name_plural = "Інформація про групи"

    def __str__(self):
        return f"Група {self.group_name}"

    @classmethod
    def get_active_info(cls):
        """Отримати активну інформацію про групу"""
        return cls.objects.filter(is_active=True).first()