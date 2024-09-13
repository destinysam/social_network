from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class FriendRequests(models.Model):
    STATUS_CHOICE = [
        ("pending","Pending"),
        ("accepted","Accepted"),
        ("rejected","Rejected"),
    ]
    request_sent_by = models.ForeignKey(User,related_name=_("sender"),on_delete=models.CASCADE,verbose_name=_("sender"))
    request_sent_to = models.ForeignKey(User,related_name=_("reciever"),on_delete=models.CASCADE,verbose_name=_("reciever"))
    status = models.CharField(verbose_name=_("status"),max_length=12,choices=STATUS_CHOICE,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        unique_together = ("request_sent_by","request_sent_to")