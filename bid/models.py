from customers.models import CustomerContact
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from equipment.models import Equipment
from labor.models import LaborHours
from materials.models import MaterialOrder
from projects.models import Project
from travel.models import TravelHours, TravelExpense


class Bid(models.Model):
    BID_TYPE_CHOICES = (
        ('Initial', 'Initial'),
        ('Additional', 'Additional'),
        ('Change Order', 'Change Order'),
        ('Time & Material', 'Time & Material'),
        ('Warranty', 'Warranty'),
    )
    BID_STATUS_CHOICES = (
        ('Generated', 'Generated'),
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
        default='Generated',
    )
    bid_due_date = models.DateField(
        verbose_name='Bid Due Date',
        db_column='bid_due_date',
        blank=True,
        null=True,
    )
    bid_due_time = models.TimeField(
        verbose_name='Bid Due Time',
        db_column='bid_due_time',
        blank=True,
        null=True,
    )
    bid_submitted = models.DateTimeField(
        verbose_name='Bid Submitted',
        db_column='bid_submitted',
        blank=True,
        null=True,
    )
    bid_submitted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Bid Submitted By',
        db_column='bid_submitted_by',
        related_name='bid_submitted_by',
        blank=True,
        null=True,
    )
    bid_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Bid Project',
        db_column='bid_project',
    )
    bid_labor_hours = models.ManyToManyField(
        LaborHours,
        verbose_name='Bid Labor Hours',
        db_column='bid_labor_hours',
        blank=True,
    )
    bid_travel_hours = models.ManyToManyField(
        TravelHours,
        verbose_name='Bid Travel Hours',
        db_column='bid_travel_hours',
        blank=True,
    )
    bid_travel_expenses = models.ManyToManyField(
        TravelExpense,
        verbose_name='Bid Travel Expenses',
        db_column='bid_travel_expenses',
        blank=True,
    )
    # bid_materials = models.ManyToManyField(
    #     Material,
    #     verbose_name='Bid Materials',
    #     db_column='bid_materials',
    #     blank=True,
    # )
    bid_material_orders = models.ManyToManyField(
        MaterialOrder,
        verbose_name='Bid Material Orders',
        db_column='bid_material_orders',
        blank=True,
    )
    bid_equipment = models.ManyToManyField(
        Equipment,
        verbose_name='Bid Equipment',
        db_column='bid_equipment',
        blank=True,
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
        if self.bid_status == 'Submitted to Customer':
            self.bid_submitted = timezone.now()
            self.bid_submitted_by = self.last_updated_by
        super(Bid, self).save(*args, **kwargs)


def create_bid(sender, instance, created, **kwargs):
    if created and instance.is_new_project:
        bid = Bid()
        if Bid.objects.filter(bid_project=instance).exists():
            # Check if there's a bid with 'Initial' bid_type
            if bid.filter(bid_project=instance, bid_type='Initial').exists():
                bid_type = 'Additional'
            else:
                bid_type = 'Initial'
        else:
            bid_type = 'Initial'
        bid.bid_type = bid_type
        bid.bid_project = instance
        bid.created_by = instance.created_by
        bid.last_updated_by = instance.created_by
        bid.save()
        # Update the instance to set is_new_project to False
        instance.is_new_project = False
        instance.save()


post_save.connect(create_bid, sender=Project)
