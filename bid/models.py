from customers.models import CustomerContact
from django.contrib.auth.models import User 
from django.db import models
from django.db.models.signals import m2m_changed
from projects.models import Project 


class Bid(models.Model):
    BID_TYPE_CHOICES = (
        ('Initial', 'Initial'),
        ('Revision', 'Revision'),
        ('Change Order', 'Change Order'),
        ('Time & Material', 'Time & Material'),
        ('Warranty', 'Warranty'),
    )
    BID_STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Approved (Internally)', 'Approved (Internally)'),
        ('Submitted to Customer', 'Submitted to Customer'),
        ('Awarded', 'Awarded'),
        ('Lost', 'Lost'),
        ('No Bid', 'No Bid'),
    )
    bid_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Bid ID',
        db_column='bid_id',
    )
    bid_type = models.CharField(
        max_length=50,
        choices=BID_TYPE_CHOICES,
        verbose_name='Bid Type',
        db_column='bid_type',
        default='Initial',
    )
    bid_status = models.CharField(
        max_length=50,
        choices=BID_STATUS_CHOICES,
        verbose_name='Bid Status',
        db_column='bid_status',
        default='Draft',
    )
    bid_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Bid Project',
        db_column='bid_project',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Bid Created On',
        db_column='bid_created_on',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Bid Created By',
        db_column='bid_created_by',
    )
    last_updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Bid Updated On',
        db_column='bid_updated_on',
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   
        verbose_name='Bid Updated By',
        db_column='bid_updated_by',
        related_name='bid_updated_by',
    )

    class Meta:
        db_table = 'bid'
        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'
        ordering = ['-created_on']

    def __str__(self):
        return str(self.bid_id)

    def save(self, user=None, *args, **kwargs):
        if user and not self.created_by:
            self.created_by = user 
        if user:
            self.last_updated_by = user 
        super(Bid, self).save(*args, **kwargs)


def create_bid(sender, instance, **kwargs):
    if 'post_add' and instance.project_status == 'Bidding' and not Bid.objects.filter(bid_project=instance).exists():
        bid = Bid()
        bid.bid_project = instance
        bid.created_by = instance.created_by
        bid.last_updated_by = instance.created_by
        bid.save()


m2m_changed.connect(create_bid, sender=Project.project_contacts.through)
