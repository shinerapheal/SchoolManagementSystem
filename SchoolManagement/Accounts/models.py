from django.db import models
from django.core.validators import RegexValidator
from django.forms import ValidationError
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import phonenumbers
from django.utils import timezone


phone_regex = RegexValidator(
        regex=r'^\d{9,15}$', 
        message="Phone number must be between 9 and 15 digits."
    )

def validate_file_size(value):
    filesize = value.size
    if filesize > 10485760:  # 10 MB
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    return value

class Country_Codes(models.Model):
    country_name = models.CharField(max_length=100,unique=True)
    calling_code = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f"{self.country_name} ({self.calling_code})"
    
    class Meta:
        ordering = ['calling_code']

class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('razorpay','razorpay'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be provided')

        # Normalize the email if provided
        if email:
            email = self.normalize_email(email)

        # Handle phone number validation if provided and not a superuser
        if phone_number and not extra_fields.get('is_superuser'):
            full_number = f"{extra_fields.get('country_code')}{phone_number}"
            try:
                parsed_number = phonenumbers.parse(full_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError("Invalid phone number.")
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise ValidationError("Invalid phone number format.")

        # Create and return the user object
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if email is None:
            raise ValueError('Superuser must have an email address.')

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)


class User(AbstractBaseUser):

    created_at = models.DateTimeField(auto_now_add=True)

    #roles
    is_librarian = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    # Any other fields common to both roles
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=30)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    place = models.CharField(max_length=20,blank=True,null=True)
    pin_code = models.CharField(max_length=10)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    joining_date = models.DateField(null=True,blank=True)
    watsapp = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True,validators=[phone_regex], null=True, blank=True)
    country_code = models.ForeignKey(Country_Codes, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    groups = models.ManyToManyField(
        Group,
        related_name='app1_user_groups',  # Add a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # Override user_permissions field with a unique related_name
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='app1_user_permissions'  # Add a unique related_name
    )
    
    def __str__(self):
        return self.email if self.email else self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class Librarian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='librarian')
    custom_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)  # Custom ID field
    profile_image = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    address_proof = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])
    adhar_id = models.CharField(max_length=255, blank=True, null=True)  

    def save(self, *args, **kwargs):
            if not self.custom_id:
               
                # Combine to form the custom ID
                self.custom_id = f'LB{self.user.id}'  # Format: LB

            super(Librarian,self).save(*args, **kwargs)
    def __str__(self):
        return self.custom_id
    
class OfficeStaff(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='staff')
    custom_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)  # Custom ID field
    profile_image = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    address_proof = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])
    adhar_id = models.CharField(max_length=255, blank=True, null=True)  
    def save(self, *args, **kwargs):
            if not self.custom_id:
               
                # Combine to form the custom ID
                self.custom_id = f'OFS{self.user.id}'  # Format: OFS

            super(OfficeStaff,self).save(*args, **kwargs)
    def __str__(self):
        return self.custom_id
    




class Student_details(models.Model):

    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='student')
    custom_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)  # Custom ID field
    profile_image = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    address_proof = models.ImageField(upload_to='s-profile-images/', null=True, blank=True, validators=[validate_file_size])
    adhar_id = models.CharField(max_length=255, blank=True, null=True)  
    def save(self, *args, **kwargs):
            if not self.custom_id:
               
                # Combine to form the custom ID
                self.custom_id = f'STU{self.user.id}'  # Format: OFS

            super(Student_details,self).save(*args, **kwargs)
    def __str__(self):
        return self.custom_id

class FeeRemark(models.Model):

    student_id = models.CharField(max_length=50,blank=True, null=True)

    fee_type = models.CharField(max_length=50,choices=PAYMENT_METHOD_CHOICES)
    amount = models.IntegerField()
    amount_payed = models.IntegerField()
    payment_date = models.DateField()
    is_payed = models.BooleanField(default=False)

class LibraryHystory(models.Model):

    student_id = models.CharField(max_length=50,blank=True, null=True)

    book_name = models.CharField(max_length=50,blank=True, null=True)
    borrow_date = models.DateField(null=True,blank=True)
    return_date = models.DateField(null=True,blank=True)
    is_returned = models.BooleanField(default=False)