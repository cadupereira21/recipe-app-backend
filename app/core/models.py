from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Since the UserManager is associated with the User model, we can use self.model to create a new user instance.
        # It is similar to calling User(email=email, **extra_fields)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Superusers must have is_staff and is_superuser set to True
        super_user = self.create_user(email, password, **extra_fields)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)

        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # This is how we associate a manager for the user model. This is used to create user instances.
    objects = UserManager()

    USERNAME_FIELD = 'email'
