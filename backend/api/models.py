import uuid
from django.db import models

# Create your models here.
class BotUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    full_name = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    twofa_password = models.CharField(max_length=64, null=True, blank=True)

    dayly_limit = models.IntegerField(default=0)
    language_code = models.CharField(max_length=8,blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    # created_at = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return f"{self.full_name} || @{self.username}"

class Comment(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    text = models.TextField()