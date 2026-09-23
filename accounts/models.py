from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    role = models.ForeignKey(
        'user_management.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role:
            if self.role.name == 'Super Admin':
                self.is_superuser = True
                self.is_staff = True
            elif self.role.name == 'Admin':
                self.is_superuser = False
                self.is_staff = True
            else:
                self.is_superuser = False
                self.is_staff = False
        else:
            self.is_superuser = False
            self.is_staff = False
            
        super().save(*args, **kwargs)