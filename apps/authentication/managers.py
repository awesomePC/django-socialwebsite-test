from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if email is None:
            raise TypeError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self,email, password, **extra_fields):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password , **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = "ADMIN"
        user.save()

        return user