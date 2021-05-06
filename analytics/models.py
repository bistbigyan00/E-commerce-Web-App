from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save

from .signals import object_viewed_signal
from accounts.signals import user_logged_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL

# Create your models here.
class ObjectViewd(models.Model):
    #instamce of the user
    user            = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    #then grab ip address
    ip_address      = models.CharField(max_length=220,blank=True,null=True)
    #this can be anything like, product, order,user,cart, any database or model
    content_type    = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    #this will be the id of record of those models/database
    object_id       = models.PositiveIntegerField()
    #with the help of model and record id, we can get object of that model, details of that object
    content_object  = GenericForeignKey('content_type','object_id')
    #session of user id
    session_id      = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s" %(self.content_object,self.timestamp)

    class Meta:
        #order by latest timestamp
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    #user)
    #get the content type of that model
    #it is same like instance.__class__, which we did in mixins
    c_type = ContentType.objects.get_for_model(sender)
    
    new_view_obj = ObjectViewd.objects.create(
                    user=request.user,
                    content_type=c_type,
                    object_id=instance.id,
                    ip_address=get_client_ip(request)
    )

object_viewed_signal.connect(object_viewed_receiver)

# Create your models here.
class UserSession(models.Model):
    #instamce of the user
    user            = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    #then grab ip address
    ip_address      = models.CharField(max_length=220,blank=True,null=True)
    session_key      = models.CharField(max_length=100, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return "%s viewed on %s" %(self.user,self.timestamp)

    #delete one single session
    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended

#once we logged in other session might be active, so we have to delete all those sessions
def post_save_delete_session(sender,instance,created,*args,**kwargs):
    if created:
        #get all the session if of user but exclude the latest session id which is just created after user logs in
        session_qs = UserSession.objects.filter(user=instance.user, ended=False,active=True).exclude(id=instance.id)
        for i in session_qs:
            i.end_session()

post_save.connect(post_save_delete_session,sender=UserSession)

def user_logged_receiver(instance,sender,request,*args,**kwargs):
    print(instance)
    ip_address = get_client_ip(request)
    user = instance
    #inbuilt request for getting session_key
    session_key = request.session.session_key

    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

#if user is logged in, send and request is already sent via accounts view to the signal
user_logged_signal.connect(user_logged_receiver)
