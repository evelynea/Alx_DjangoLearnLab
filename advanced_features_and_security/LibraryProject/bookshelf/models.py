from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):

    date_of_birth = models.DateField()
    profile_photo = models.ImageField(upload_to='profile_photo/')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.username
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, profile_photo=None, password=None):
        if not email:
            raise ValueError("Usera must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            profile= profile_photo
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, profile_photo=None, password=None):
        user = self.create_superuser(
            email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        