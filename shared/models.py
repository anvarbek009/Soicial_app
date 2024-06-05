from django.db import models
from shared.models import UIDMixin

class UserProfile(UIDMixin):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/')
    
    def __str__(self):
        return f"{self.user.username} - {self.uid}"
