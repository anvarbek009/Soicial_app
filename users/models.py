import datetime
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import imghdr
from shared.models import BaseModel
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
ORDINARY_USER , ADMIN,MANAGER =('ordinary_user', 'admin', 'manager')
VIA_EMAIL,VIA_PHONE=('via_email', 'via_phone')
NEW,CONFIRM,DONE,DONE_PHOTO=('new', 'confirm', 'done', 'done_photo')
MALE,FEMALE,OTHER = ('male', 'female', 'other')

def validate_image(file):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']

    mime_type = file.file.content_type
    if mime_type not in valid_mime_types:
        raise ValidationError(f"Unsupported file type. Allowed types are: {', '.join(valid_extensions)}.")

    ext = imghdr.what(file)
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extensions)}.")

    max_size_kb = 2048
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"Image file size should not exceed {max_size_kb} KB.")

    max_width, max_height = 3000, 3000
    width, height = get_image_dimensions(file)
    if width > max_width or height > max_height:
        raise ValidationError(f"Image dimensions should not exceed {max_width}x{max_height} pixels.") 

class User(AbstractUser, BaseModel):
    USER_TYPE=(
        (ORDINARY_USER, ORDINARY_USER),
        (ADMIN, ADMIN),
        (MANAGER, MANAGER),
    )
    user_role = models.CharField(max_length=50, choices=USER_TYPE, default=ORDINARY_USER)
    
    GENDER_TYPE=(
        (MALE, MALE),
        (FEMALE, FEMALE),
        (OTHER, OTHER),
    )

    USER_STATUS = [
        (NEW, NEW),
        (CONFIRM, CONFIRM),
        (DONE, DONE),
        (DONE_PHOTO, DONE_PHOTO),
    ]

    AUTH_TYPE =[
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    ]
    gender = models.CharField(max_length=50, choices=GENDER_TYPE, default=MALE)
    profile_image = models.ImageField(upload_to='profile_images/', validators=[validate_image])
    
    @property
    def full_name(self):
        return f'{self.first_name} - {self.last_name}'
    
    def create_verify_code(self):
        code =''.join([str(random.randint(0, 100)%10) for _ in range(4)])
        ConfirmUser.objects.create(
            user_id=self.id,
            verity_type=self.auth_type,
            code=code        
        )
        return code
    
    def username_validate(self):
        if not self.username:
            temp_password = f'password-{uuid.uuid4().__str__().split('-')[-2]}'
            self.password = temp_password

        
  
    def email_validate(self):
        normalized_email=self.email.lower()
        self.email = normalized_email

    def password_validate(self):
        if not self.password:
            temp_username = f'social{uuid.uuid4().__str__().split('-')[-1]}'
            while User.objects.filter(username=temp_username):
                temp_username = f'{temp_username}{str(random.randint(1,100))}'
            self.username = temp_username
    
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh=RefreshToken.for_user(self.user)

    def clean(self):
        self.username_validate()
        self.email_validate()
        self.password_validate()
        self.hashing_password()

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(**args, **kwargs)
EMAIL_EXPIRE = 3
PHONE_EXPIRE = 2

class ConfirmUser(BaseModel):
    VERITY_TYPE = [
        (VIA_EMAIL,VIA_EMAIL)
        (VIA_PHONE,VIA_PHONE)
    ]
    verify_type=models.CharField(max_length=50,choices=VERITY_TYPE)
    code=models.CharField(max_length=4)
    expiration_time=models.DateTimeField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} {self.verify_type} - {self.code}"
    
    # def save(self):
