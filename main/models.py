from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_practitioner = models.BooleanField(default=False)
    practitioner = models.ForeignKey(
        User, related_name='patient_practitioner', 
        on_delete=models.CASCADE, blank=True, null=True
	) 
@receiver(post_save, sender=User, dispatch_uid="create_or_update_user_profile_signal")
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Practitioner(Profile):
    class Meta:
        proxy = True


class Patient(Profile):
    class Meta:
        proxy = True