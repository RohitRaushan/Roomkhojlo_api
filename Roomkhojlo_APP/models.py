
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomTenantManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        tenant = self.model(email=email, **extra_fields)
        tenant.set_password(password)
        tenant.save()
        return tenant

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Tenant(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150, unique=True)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='tenant_photos/', default='tenant_photos/default.jpg', null=True, blank=True)
    role=models.CharField(max_length=100, default='tenant')
    emp_id = models.CharField(max_length=150, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['name']

    objects = CustomTenantManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tenant'
        verbose_name = 'tenant'
        verbose_name_plural = 'tenants'


class CustomLandlordManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        landlord = self.model(email=email, **extra_fields)
        landlord.set_password(password)
        landlord.save()
        return landlord

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Landlord(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150, unique=True)
    alternate_contact = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='landlord_photos', default='landlord_photos/default.jpg', null=True, blank=True)
    id_proof_type = models.CharField(max_length=150)
    id_proof_number = models.CharField(max_length=150)
    role=models.CharField(max_length=100, default='landlord')
    token = models.CharField(max_length=255, null=True, blank=True)
    emp_id =models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['name']

    objects = CustomLandlordManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'landlord'
        verbose_name = 'landlord'
        verbose_name_plural = 'landlords'


class CustomEmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        employee = self.model(email=email, **extra_fields)
        employee.set_password(password)
        employee.save()
        return employee

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Employee(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150,unique=True)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    salary = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='employee_photos/', default='employee_photos/default.jpg', null=True, blank=True)
    role = models.CharField(max_length=50, default='employee')
    token = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['name']

    objects = CustomEmployeeManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employee'
        verbose_name = 'employee'
        verbose_name_plural = 'employees'


class CustomAgentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        agent = self.model(email=email, **extra_fields)
        agent.set_password(password)
        agent.save()
        return agent

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Agent(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    agency_name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150,unique=True)
    alternate_contact = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='agent_photos/', default='agent_photos/default.jpg', null=True, blank=True)
    id_proof_type = models.CharField(max_length=150)
    id_proof_number = models.CharField(max_length=150)
    role=models.CharField(max_length=100, default='agent')
    emp_id = models.CharField(max_length=50, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['name']

    objects = CustomAgentManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'agent'
        verbose_name = 'agent'
        verbose_name_plural = 'agents'



class enquiry(models.Model):
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150,unique=True)
    email = models.CharField(max_length=150,unique=True)
    room_type = models.CharField(max_length=255)
    location = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    assigned_to = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=10, choices=(('active', 'active'), ('inactive', 'inactive')), default='active')    
    emp_id = models.CharField(max_length=150, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'table_enquiry'
        verbose_name = 'enquiry'
        verbose_name_plural = 'enquiries'

class Building(models.Model):
    landlord_id = models.CharField(max_length=150, null=True, blank=True)
    building_name = models.CharField(max_length=150)
    building_type = models.CharField(max_length=150)
    room_type = models.CharField(max_length=150)
    gender= models.CharField(max_length=10)
    amenities = models.CharField(max_length=255, null=True, blank=True)
    furnishing_status = models.CharField(max_length=150, null=True, blank=True)
    photo=models.ImageField(upload_to='building_photos/', default='building_photos/default.jpg', null=True, blank=True) 
    total_floors = models.CharField(max_length=150)
    total_rooms = models.CharField(max_length=150)
    min_rent = models.CharField(max_length=150, null=True, blank=True)
    max_rent = models.CharField(max_length=150, null=True, blank=True)
    locality = models.CharField(max_length=150)
    state=models.CharField(max_length=150)
    city=models.CharField(max_length=150)
    district=models.CharField(max_length=150)
    street_address=models.CharField(max_length=150)
    pincode=models.CharField(max_length=150)
    lattitude=models.CharField(max_length=150, null=True, blank=True)
    longitude=models.CharField(max_length=150, null=True, blank=True)
    availability_status =models.CharField(max_length=150)
    emp_id = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.building_name
    
    class Meta:
        db_table = 'tbl_building'

class Booking(models.Model):
    building_id = models.CharField(max_length=150)
    agent_id = models.CharField(max_length=150, null=True, blank=True)
    emp_id = models.CharField(max_length=150, null=True, blank=True)
    tenant_id = models.CharField(max_length=150, null=True, blank=True)
    landlord_id = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150,unique=True)
    contact = models.CharField(max_length=15,unique=True)
    booking_date = models.DateTimeField()
    check_in_date = models.DateTimeField()
    duration_of_stay = models.CharField(max_length=150, null=True, blank=True)
    rent_amt = models.CharField(max_length=150)
    deposit_amt = models.CharField(max_length=150)
    room_type = models.CharField(max_length=150, null=True, blank=True)
    booking_status = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'booking_details'

class Payment(models.Model):
    booking_id =models.CharField(max_length=150)
    payment_amt = models.CharField(max_length=150)
    payment_mode = models.CharField(max_length=150)
    payment_status = models.CharField(max_length=150)
    payment_date = models.DateTimeField()
    emp_id = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment_details'

class Review(models.Model):
    building_id = models.CharField(max_length=150, null=True, blank=True)
    tenant_id = models.CharField(max_length=150, null=True, blank=True)
    emp_id = models.CharField(max_length=150, null=True, blank=True)
    rating = models.CharField(max_length=150)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'review_details'
