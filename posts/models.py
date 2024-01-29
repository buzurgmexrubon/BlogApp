import os
from datetime import datetime, timedelta, timezone

from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse

from core import models as core_models
from users import models as user_models


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="post_photos")
    post = models.ForeignKey("Post", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


@receiver(post_delete, sender=Photo)
def file_delete_action(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(pre_save, sender=Photo)
def file_update_action(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False

    for field in instance._meta.fields:
        field_type = field.get_internal_type()
        if field_type == "FileField" or field_type == "ImageField":
            origin_file = getattr(old_obj, field.name)
            new_file = getattr(instance, field.name)
            print(origin_file, new_file)
            if origin_file != new_file and os.path.isfile(origin_file.path):
                os.remove(origin_file.path)


class Post(core_models.TimeStampedModel):

    """Post Model Definition"""

    author = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.author}"

    # TODO
    def comments_count(self):
        commentCount = self.post_comments.count()
        return int(commentCount)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def created_string(self):
        created_time = datetime.now(tz=timezone.utc) - self.created

        if created_time < timedelta(minutes=1):
            return "Just before"
        elif created_time < timedelta(hours=1):
            return str(int(created_time.seconds / 60)) + " minutes ago"
        elif created_time < timedelta(days=1):
            return str(int(created_time.seconds / 3600)) + " hours ago"
        else:
            created_time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(created_time.days) + " days ago"
