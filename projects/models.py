from customers.models import CustomerContact
from datetime import date, datetime
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import m2m_changed
from notes.models import Note
from sites.models import Site


class Project(models.Model):
    PROJECT_STATUS_CHOICES = (
        ('Bidding', 'Bidding'),
        ('Planning', 'Planning'),
        ('Active', 'Active'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    project_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Project ID',
        db_column='project_id',
    )
    project_name = models.CharField(
        max_length=100,
        verbose_name='Project Name',
        db_column='project_name',
    )
    project_number = models.CharField(
        max_length=100,
        verbose_name='Project Number',
        db_column='project_number',
        help_text='Provided by the Customer',
        default='Pending',
    )
    project_status = models.CharField(
        max_length=50,
        choices=PROJECT_STATUS_CHOICES,
        verbose_name='Project Status',
        db_column='project_status',
        default='Bidding',
    )
    project_contacts = models.ManyToManyField(
        CustomerContact,
        verbose_name='Project Contacts',
        db_column='project_contacts',
    )
    project_start = models.DateField(
        verbose_name='Project Start',
        db_column='project_start',
        default=datetime.date(datetime.now()),
    )
    project_end = models.DateField(
        verbose_name='Project End',
        db_column='project_end',
        default=datetime.date(datetime.now()),
    )
    project_sites = models.ManyToManyField(
        Site,
        verbose_name='Project Sites',
        db_column='project_sites',
        help_text='All Sites Associated with the Project',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Project Created On',
        db_column='project_created_on',
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Project Created By',
        db_column='project_created_by',
    )
    last_updated_on = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated On',
        db_column='last_updated_on',
    )
    last_updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Last Updated By',
        db_column='last_updated_by',
        related_name='project_last_updated_by'
    )
    project_notes = models.ManyToManyField(
        Note,
        verbose_name='Project Notes',
        db_column='project_notes',
        blank=True,
    )
    is_new_project = models.BooleanField(
        default=True,
        verbose_name='Is New Project',
        db_column='is_new_project',
    )

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-project_start']

    def __str__(self):
        return f'({self.project_number}) {self.project_name}'

    def save(self, user=None, *args, **kwargs):
        if user and not self.created_by:
            self.created_by = user
        if user:
            self.last_updated_by = user
        super(Project, self).save(*args, **kwargs)
        return user
