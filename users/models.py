# from django.contrib.auth.models import User
# from collections.abc import Iterable
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls.base import reverse
from PIL import Image


class Profile(models.Model):
    # user = models.OneToOneField("User", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.jpg", upload_to="avatar")

    # def __str__(self):
    #     return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class User(AbstractUser):
    # profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    """User Model Definition"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    )

    # first_name = models.CharField(max_length=100)
    # second_name = models.CharField(max_length=100)
    # avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, null=True, blank=True
    )
    bio = models.TextField(default="", blank=True)
    superhost = models.BooleanField(default=False)

    # def get_absolute_url(self):
    #     return reverse("users:profile", kwargs={"pk": self.pk})
