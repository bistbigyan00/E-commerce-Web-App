from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

#for creating the billing profile after creating the user or guest provide the email
class BillingManager(models.Manager):

    def new_or_get(self,request):
        obj = None
        created = False
        user = request.user
        guest_email_id = request.session.get('guest_email_id')

        if user.is_authenticated:
            obj,created = BillingProfile.objects.get_or_create(user=user,email=user.email)

        elif guest_email_id is not None:
            guest_obj = GuestEmail.objects.get(id=guest_email_id)
            obj,created = BillingProfile.objects.get_or_create(email=guest_obj.email)
        else:
            pass
        #createed will always be true if get_or_create runs, but it doesnot run, we setup it as false
        return obj, created

# Create your models here.
class BillingProfile(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingManager()

    def __str__(self):
        return self.email

#after user is created, save the billing profile
def post_save_billingprofile(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(post_save_billingprofile,sender=User)
