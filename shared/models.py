from django.db import models
from shared.models import UIDMixin
import uuid

class UserProfile(UIDMixin):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/')
    
    def __str__(self):
        return f"{self.user.username} - {self.uid}"
    
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4(),unique=True,editable=False,primary_key=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return super().__str__()
