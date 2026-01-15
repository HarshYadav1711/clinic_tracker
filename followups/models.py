from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import generate_code, generate_token

#Created Clinic Model
class Clinic(models.Model):
    name = models.CharField(max_length=255)
    clinic_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.clinic_code:
            self.clinic_code = generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

#Created UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
#Created FollowUp model
class FollowUp(models.Model):
    LANG_CHOICES = [("en", "English"), ("hi", "Hindi")]
    STATUS_CHOICES = [("pending", "Pending"), ("done", "Done")]

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    language = models.CharField(max_length=2, choices=LANG_CHOICES)
    notes = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    public_token = models.CharField(max_length=40, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.public_token:
            self.public_token = generate_token()
        super().save(*args, **kwargs)


#Created PublicView log
class PublicViewLog(models.Model):
    followup = models.ForeignKey(FollowUp, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now)
    user_agent = models.TextField(blank=True)
    ip_address = models.CharField(max_length=45, blank=True)
