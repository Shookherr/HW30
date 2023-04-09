from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    name = models.CharField('Название', max_length=256, unique=True)
    lat = models.DecimalField('Широта', max_digits=8, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField('Долгота', max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class UserRoles(models.TextChoices):
    MEMBER = 'member', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    role = models.CharField(choices=UserRoles.choices, max_length=9, default=UserRoles.MEMBER)
    age = models.PositiveSmallIntegerField(null=True)
    location = models.ManyToManyField(Location)

    def save(self, *args, **kwargs):
        self.set_password(raw_password=self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
