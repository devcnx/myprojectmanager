from django.db import models


class ResourceStatus(models.Model):
    resource_status_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Resource Status ID',
        db_column='resource_status_id',
    )
    resource_status = models.CharField(
        max_length=30,
        verbose_name='Resource Status',
        db_column='resource_status',
    )

    class Meta:
        db_table = 'resource_statuses'
        verbose_name = 'Resource Status'
        verbose_name_plural = 'Resource Statuses'
        ordering = ['resource_status']

    def __str__(self):
        return self.resource_status


class ResourceCompany(models.Model):
    resource_company_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Resource Company ID',
        db_column='resource_company_id',
    )
    resource_company = models.CharField(
        max_length=30,
        verbose_name='Resource Company',
        db_column='resource_company',
    )

    class Meta:
        db_table = 'resource_companies'
        verbose_name = 'Resource Company'
        verbose_name_plural = 'Resource Companies'
        ordering = ['resource_company']

    def __str__(self):
        return self.resource_company


class Resource(models.Model):
    resource_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Resource ID',
        db_column='resource_id',
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='First Name',
        db_column='first_name',
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='Last Name',
        db_column='last_name',
    )
    work_phone = models.CharField(
        max_length=20,
        verbose_name='Work Phone',
        db_column='work_phone',
        blank=True,
        null=True,
    )
    cell_phone = models.CharField(
        max_length=20,
        verbose_name='Cell Phone',
        db_column='cell_phone',
        blank=True,
        null=True,
    )
    email = models.EmailField(
        max_length=255,
        verbose_name='Email',
        db_column='email',
        blank=True,
        null=True,
    )
    is_project_manager = models.BooleanField(
        default=False,
        verbose_name='Is Project Manager',
        db_column='is_project_manager',
    )
    is_low_voltage = models.BooleanField(
        default=False,
        verbose_name='Is Low Voltage',
        db_column='is_low_voltage',
    )
    is_electrician = models.BooleanField(
        default=False,
        verbose_name='Is Electrician',
        db_column='is_electrician',
    )
    is_combo_technician = models.BooleanField(
        default=False,
        verbose_name='Is Combo Technician',
        db_column='is_combo_technician',
    )
    is_partner = models.BooleanField(
        default=False,
        verbose_name='Is Partner',
        db_column='is_partner',
    )
    is_field_personnel_only = models.BooleanField(
        default=False,
        verbose_name='Is Field Personnel Only',
        db_column='is_field_personnel_only',
    )
    is_office_personnel_only = models.BooleanField(
        default=False,
        verbose_name='Is Office Personnel Only',
        db_column='is_office_personnel_only',
    )
    is_combo_personnel = models.BooleanField(
        default=False,
        verbose_name='Is Combo Personnel',
        db_column='is_combo_personnel',
    )
    resource_company = models.ForeignKey(
        ResourceCompany,
        on_delete=models.CASCADE,
        verbose_name='Resource Company',
        db_column='resource_company_id',
    )
    resource_status = models.ForeignKey(
        ResourceStatus,
        on_delete=models.CASCADE,
        default='1',
        verbose_name='Resource Status',
        db_column='resource_status_id',
    )

    class Meta:
        db_table = 'resources'
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
