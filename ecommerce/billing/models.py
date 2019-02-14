from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL


class BillinigProfileManager(models.Manager):
    def new_or_get(self,request):
        user = request.user
        guest_email_id = request.session.get("guest_email_id")
        billing_profile = None
        created = False
        if user.is_authenticated:
            billing_profile, created = self.model.objects.get_or_create(user=user,email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            billing_profile, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        return billing_profile , created


class BillinigProfile(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillinigProfileManager()

    def __str__(self):
        return self.email


def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillinigProfile.objects.get_or_create(user=instance,email=instance.email)


post_save.connect(user_created_receiver,sender=User)