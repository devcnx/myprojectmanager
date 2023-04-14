from django.contrib.auth.models import User 
from django.db import models



class Bid(models.Model):
    BID_TYPE_CHOICES = (
        ('Initial', 'Initial'),
        ('Revision', 'Revision'),
        ('Change Order', 'Change Order'),
        ('Time & Material', 'Time & Material'),
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
    bid_created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Bid Created On',
        db_column='bid_created_on',
    )
    bid_created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Bid Created By',
        db_column='bid_created_by',
    )
    bid_updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Bid Updated On',
        db_column='bid_updated_on',
    )
    bid_updated_by = models.ForeignKey(
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
        ordering = ['-bid_created_on']

    def __str__(self):
        return str(self.bid_id)




