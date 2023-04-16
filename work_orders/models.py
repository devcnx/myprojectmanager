from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from notes.models import Note
from projects.models import Project
from resources.models import Resource
from sites.models import Site
# from trips.models import Trip


class WorkOrder(models.Model):
    WORK_ORDER_STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Cancelled', 'Cancelled'),
    )
    work_order_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Work Order ID',
        db_column='work_order_id',
    )
    work_order_number = models.CharField(
        max_length=50,
        verbose_name='Work Order Number',
        db_column='work_order_number',
    )
    work_order_status = models.CharField(
        max_length=50,
        choices=WORK_ORDER_STATUS_CHOICES,
        verbose_name='Work Order Status',
        db_column='work_order_status',
        default='Open',
    )
    work_order_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='Work Order Project',
        db_column='work_order_project',
    )
    work_order_site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name='Work Order Site',
        db_column='work_order_site',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Work Order Created On',
        db_column='work_order_created_on',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Work Order Created By',
        db_column='work_order_created_by',
        related_name='work_order_created_by',
    )
    last_updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Work Order Last Updated On',
        db_column='work_order_last_updated_on',
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Work Order Last Updated By',
        db_column='work_order_last_updated_by',
        related_name='work_order_last_updated_by',
    )
    work_order_notes = models.ManyToManyField(
        Note,
        verbose_name='Work Order Notes',
        db_column='work_order_notes',
        blank=True,
    )

    class Meta:
        db_table = 'work_orders'
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        ordering = ['-created_on']

    def __str__(self):
        return str(self.work_order_number)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().save(*args, **kwargs)

    @staticmethod
    def get_next_work_order_number():
        year = datetime.now().year
        month = datetime.now().month

        # Get the instance's last work order
        last_work_order = WorkOrder.objects.filter(
            work_order_number__startswith=f'WO {year}'
        ).order_by('-work_order_number').first()

        # If there is a last work order, get the last work order number and increment it by 1
        if last_work_order:
            last_work_order_number = last_work_order.work_order_number
            last_work_order_number = last_work_order_number.split('-')[1]
            next_work_order_number = int(last_work_order_number) + 1
        else:
            next_work_order_number = 1

        # Return the next work order number
        return f'WO {year}-{next_work_order_number:04d}-{month:02d}'


# Create a work order for each site in a project (project_sites - many to many)
@receiver(m2m_changed, sender=Project.project_sites.through)
def create_work_order_for_project_sites(sender, instance, action, **kwargs):
    if action == 'post_add':
        if instance.project_status in ['Planning', 'Active']:
            for site in instance.project_sites.all():
                if not WorkOrder.objects.filter(work_order_project=instance, work_order_site=site).exists():
                    next_work_order_number = WorkOrder.get_next_work_order_number()
                    WorkOrder.objects.create(
                        work_order_number=next_work_order_number,
                        work_order_project=instance,
                        work_order_site=site,
                        created_by=instance.created_by,
                        last_updated_by=instance.last_updated_by,
                    )


# If a project's status is changed to 'Planning' or 'Active', create a work order for each site in the project
# if a work order does not already exist
@receiver(post_save, sender=Project)
def update_work_order_for_project_sites_on_project_status_change(sender, instance, created, **kwargs):
    if not created:
        if instance.project_status in ['Planning', 'Active']:
            for site in instance.project_sites.all():
                if not WorkOrder.objects.filter(work_order_project=instance, work_order_site=site).exists():
                    next_work_order_number = WorkOrder.get_next_work_order_number()
                    WorkOrder.objects.create(
                        work_order_number=next_work_order_number,
                        work_order_project=instance,
                        work_order_site=site,
                        created_by=instance.created_by,
                        last_updated_by=instance.last_updated_by,
                    )


class WorkOrderTrip(models.Model):
    TRIP_STATUS_CHOICES = (
        ('Needs Scheduled', 'Needs Scheduled'),
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Completed - Needs Additional Trip', 'Completed - Needs Additional Trip'),
        ('Cancelled', 'Cancelled'),
    )
    trip_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Trip ID',
        db_column='trip_id',
    )
    trip_number = models.PositiveIntegerField(
        editable=False,
        verbose_name='Trip Number',
        db_column='trip_number',
    )
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        verbose_name='Work Order',
        db_column='work_order',
    )
    trip_status = models.CharField(
        max_length=50,
        choices=TRIP_STATUS_CHOICES,
        verbose_name='Trip Status',
        db_column='trip_status',
        default='Needs Scheduled',
    )
    trip_start_date = models.DateField(
        verbose_name='Trip Start Date',
        db_column='trip_start_date',
        blank=True,
        null=True,
    )
    trip_start_time = models.TimeField(
        verbose_name='Trip Start Time',
        db_column='trip_start_time',
        blank=True,
        null=True,
    )
    trip_end_date = models.DateField(
        verbose_name='Trip End Date',
        db_column='trip_end_date',
        blank=True,
        null=True,
    )
    trip_end_time = models.TimeField(
        verbose_name='Trip End Time',
        db_column='trip_end_time',
        blank=True,
        null=True,
    )
    trip_project_manager = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Trip Project Manager',
        db_column='trip_project_manager',
        limit_choices_to={'is_project_manager': True},
        related_name='trip_project_manager',
    )
    trip_lead = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Trip Lead',
        db_column='trip_lead',
        related_name='trip_lead',
    )
    trip_resources = models.ManyToManyField(
        Resource,
        verbose_name='Trip Resources',
        db_column='trip_resources',
        blank=True,
        related_name='trip_resource',
    )
    trip_notes = models.ManyToManyField(
        Note,
        verbose_name='Trip Notes',
        db_column='trip_notes',
        blank=True,
        related_name='trip_note',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        db_column='created_on',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Created By',
        db_column='created_by',
        related_name='trip_created_by',
    )
    updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated On',
        db_column='updated_on',
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Updated By',
        db_column='updated_by',
        related_name='trip_updated_by',
    )

    class Meta:
        db_table = 'work_order_trips'
        verbose_name = 'Work Order Trip'
        verbose_name_plural = 'Work Order Trips'
        ordering = ['trip_start_date', 'trip_start_time']

    def __str__(self):
        return str(self.trip_number)

    def save(self, *args, **kwargs):
        if not self.trip_number:
            # Get the number of existing trips for a work order
            existing_trips = WorkOrderTrip.objects.filter(
                work_order=self.work_order).count()
            # Set the trip number to the next available number
            self.trip_number = existing_trips + 1
        user = kwargs.pop('user', None)
        super(WorkOrderTrip, self).save(*args, **kwargs)
