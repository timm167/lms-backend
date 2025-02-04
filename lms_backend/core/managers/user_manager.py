from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, role='student', email=None, **extra_fields):
        """
        Create and return a regular user with the associated role model.
        """
        from core.models import Student, Teacher, Admin

        # Re-validate the fields in backend
        if not username:
            raise ValueError('The username must be set')
        if not password:
            raise ValueError('The password must be set')
        if not email:
            raise ValueError('The email must be set')
        
        if role == 'admin':
            extra_fields.setdefault('is_staff', True)

        # Create the user instance
        user = self.model(username=username, role=role, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create the related role model based on the user role
        if role == 'student':
            Student.objects.get_or_create(user=user)
        elif role == 'teacher':
            Teacher.objects.get_or_create(user=user)
        elif role == 'admin':
            Admin.objects.get_or_create(user=user)
        
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, role='admin', **extra_fields)