from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        """Create and saves a Regular user with the given first_name, last_name, email, and password"""
        if not email:
            raise ValueError('Email address is required.')
        if not first_name:
            raise ValueError('Last name is required.')
        if not last_name:
            raise ValueError('First name is required.')

        email=self.normalize_email(email)

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """Create and saves a Superuser with the given first_name, last_name, email, and password"""
        # add extra_fields for permission
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(first_name, last_name, email, password, **extra_fields)