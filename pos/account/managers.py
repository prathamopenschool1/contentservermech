from django.contrib.auth.models import BaseUserManager


class CrlUserManager(BaseUserManager):

    def create_user(self, username, password=None):

        if not username:
            raise ValueError("Please Enter a UserName!!")

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
