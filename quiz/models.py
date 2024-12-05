import random
import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q


class BaseModelClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Shop(BaseModelClass):
    name = models.CharField(max_length=255)
    abut = models.CharField(max_length=255)
    amount = models.IntegerField()
    coin = models.IntegerField()
    image = models.ImageField(upload_to='shop/')
    is_active = models.BooleanField(default=False)
    sale = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name


class Users(AbstractUser, BaseModelClass):
    class UserAdmin(models.TextChoices):
        USER = 'user', "User"
        ADMIN = 'admin', 'Admin'

    class Level(models.TextChoices):
        Beginner = 'beginner', 'Beginner'
        Elementary = 'elementary', 'Elementary'
        Intermediate = 'intermediate', 'Intermediate'
        Advanced = 'advanced', 'Advanced'

    date_of_birth = models.DateField(default="2000-01-01")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    roles = models.CharField(max_length=25, choices=UserAdmin.choices, default=UserAdmin.USER)
    degree = models.CharField(max_length=25, choices=Level.choices, default=Level.Beginner)
    ball = models.IntegerField(default=0)
    gift = models.ManyToManyField(Shop, related_name='users')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def create_verification_code(self):
        code = "".join([str(random.randint(1, 9)) for _ in range(4)])
        UserConfig.objects.create(
            code=code,
            user_id=self.id,
            expire_time=datetime.datetime.now() + datetime.timedelta(minutes=10)
        )

        return code

    def token(self):
        access = RefreshToken.for_user(self)
        data = {
            'access_token': str(access.access_token),
            'refresh_token': str(access)
        }
        return data


class UserConfig(BaseModelClass):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='code')
    code = models.IntegerField()
    expire_time = models.DateTimeField()
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.code}'


class Sciences(BaseModelClass):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Test(BaseModelClass):
    class Degree(models.TextChoices):
        Easy = 'easy', 'Easy'
        Normal = 'normal', 'Normal'
        Hard = 'hard', 'Hard'

    name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, choices=Degree.choices)
    about = models.CharField(max_length=255, null=True, blank=True)
    sciences = models.ForeignKey(Sciences, on_delete=models.CASCADE, related_name='test')

    def __str__(self):
        return self.name


class Questions(BaseModelClass):
    about = models.CharField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.test.name


class Variants(BaseModelClass):
    text = models.CharField(max_length=255)
    is_true = models.BooleanField(default=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='variants')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question'],
                condition=Q(is_true=True),
                name='unique_true_variant_per_question'
            )
        ]

    def __str__(self):
        return self.text


