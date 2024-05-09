from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    license_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} - {self.company.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    is_company_admin = models.BooleanField(default=False)
    is_branch_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Device(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    check_out_time = models.DateTimeField(auto_now_add=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    condition_on_checkout = models.TextField()
    condition_on_checkin = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.device.name} - {self.employee.user.username}"