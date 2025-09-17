from django.db import models
from django.conf import settings
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=256,blank=False ,null=False)
    content = models.CharField(max_length=256, blank=True, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    tags = models.JSONField(default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

