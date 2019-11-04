from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date
from django.utils import timezone


class UserManager(BaseUserManager):
	def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		if not full_name:
			raise ValueError("Users must have a full name")
			
		user_obj = self.model(email = self.normalize_email(email), full_name = full_name)
		user_obj.set_password(password) #change user password
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj
	
	def create_staffuser(self, email, full_name, password=None):
		user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
		)
		return user
		
	def create_superuser(self, email, full_name, password=None):
		user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True
		)
		return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #staff user non superuser
    admin = models.BooleanField(default=False) #superuser
	
    USERNAME_FIELD = 'email' #username
	#USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['full_name']
	
    objects = UserManager()
	
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.IntegerField(blank=False, null=False, default=00000)
    phonenumber = models.IntegerField(blank=False, null=False, default=0000000000)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return self.email
		
    def get_short_name(self):
        return self.email
	
    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    # def __str__(self):
        # return str(self.username)
		
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
		
    @property
    def is_staff(self):
        return self.staff
		
    @property
    def is_admin(self):
        return self.admin
		
    @property
    def is_active(self):
        return self.active

class Roles(models.Model):
    role = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "CustomRole"
        verbose_name_plural = "CustomRoles"


class Managers(models.Model):
    # add unique constraint for id later
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managers')
    #full_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

	
class Organization(models.Model):
    # add unique constraint for id later
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=30)
    city = models.CharField(max_length=20, default='Omaha')
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)
    phone = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return str(self.organization_id)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class Volunteer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	
	def __str__(self):
		return str(self.user)


class Opportunity(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    time = models.TimeField()




    def __str__(self):
        return "Volunteer Opportunity on %s %s with %s" % (self.date, self.time, self.organization)	

	
class Assignment(models.Model):
	#organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
	opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
	status = models.IntegerField(default=0)
	
	class Meta:
		unique_together = (('volunteer', 'opportunity'),)

	def __str__(self):
		#org = Organization.objects.get(id=self.organization_id)
		vol = Volunteer.objects.get(id=self.volunteer_id)
		tim = Opportunity.objects.get(id=self.opportunity_id)
		return '%s at %s' % (vol, tim)


class Availability(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    time = models.TimeField()
	
    def __str__(self):
        return "Availability for %s at %s" % (self.opportunity, self.time)