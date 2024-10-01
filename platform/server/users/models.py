from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    is_reviewer = models.BooleanField(default=False)

class Publication(models.Model):
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE, 
                             related_name='past_publications')
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    # publication_date = models.DateField(default=lambda: timezone.now().date())
    publication_date = models.DateField()
    categories = models.JSONField(blank=True, default=list)
    
    def __str__(self):
        return self.title