from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'Користувач'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Адміністратор'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    email_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def is_admin(self) -> bool:
        return self.role == self.Roles.ADMIN

    def is_moderator(self) -> bool:
        return self.role == self.Roles.MODERATOR

    def is_user(self) -> bool:
        return self.role == self.Roles.USER


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default.jpg')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Профіль користувача {self.user.username}"

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def age(self) -> int:
        today = timezone.now().date()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
