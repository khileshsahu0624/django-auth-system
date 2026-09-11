from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == self.Role.SUPER_ADMIN:
            self.is_superuser = True
            self.is_staff = True
        elif self.role == self.Role.ADMIN:
            self.is_superuser = False
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
            
        super().save(*args, **kwargs)