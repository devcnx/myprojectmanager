from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from notes.models import Note
from projects.models import Project
from resources.models import Resource
from sites.models import Site
from trips.models import Trip


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
    work_order_trips = models.ManyToManyField(
        Trip,
        verbose_name='Work Order Trips',
        db_column='work_order_trips',
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
    )
    work_order_resources = models.ManyToManyField(
        Resource,
        verbose_name='Work Order Resources',
        db_column='work_order_resources',
    )

    class Meta:
        db_table = 'work_orders'
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        ordering = ['-created_on']

    def __str__(self):
        return str(self.work_order_number)

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
        # else:
        #     # Add a note to the instance
        #     note = Note()
        #     note.note = f'The project status was changed to {instance.project_status}.'
        #     note.author = instance.last_updated_by
        #     note.created_on = datetime.now()
        #     note.save()

        #     # Add the note to the instance
        #     instance.project_notes.add(note)
