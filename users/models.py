from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import imghdr

# Create your models here.
ORDINARY_USER , ADMIN,MANAGER =('ordinary_user', 'admin', 'manager')
VIA_EMAIL,VIA_PHONE=('via_email', 'via_phone')
NEW,CONFIRM,DONE,DONE_PHOTO=('new', 'confirm', 'done', 'done_photo')
MALE,FEMALE,OTHER = ('male', 'female', 'other')

def validate_image(file):
    # Allowed file types
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']

    # Validate file type
    mime_type = file.file.content_type
    if mime_type not in valid_mime_types:
        raise ValidationError(f"Unsupported file type. Allowed types are: {', '.join(valid_extensions)}.")

    # Further validate using imghdr to check file header
    ext = imghdr.what(file)
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extensions)}.")

    # Check file size (limit to 2MB)
    max_size_kb = 2048
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"Image file size should not exceed {max_size_kb} KB.")

    # Check image dimensions (limit to 3000x3000 pixels)
    max_width, max_height = 3000, 3000
    width, height = get_image_dimensions(file)
    if width > max_width or height > max_height:
        raise ValidationError(f"Image dimensions should not exceed {max_width}x{max_height} pixels.") 

class User(AbstractUser):
    USER_TYPE= (
        (ORDINARY_USER, ORDINARY_USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER),
    )
    user_role = models.CharField(max_length=50, choices=USER_TYPE, default=ORDINARY_USER)
    GENDER_TYPE =(
        (MALE, MALE),
        (FEMALE, FEMALE),
        (OTHER, OTHER),
    )
    gender = models.CharField(max_length=50, choices=GENDER_TYPE, default=MALE)
    profile_image = models.ImageField(upload_to='profile_images/', validators=[validate_image])
    