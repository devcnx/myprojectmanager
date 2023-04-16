from django.contrib.auth.models import User
from django.db import models
from vendors.models import Vendor


class Material(models.Model):
    material_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Material ID',
        db_column='material_id',
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Description',
        db_column='description',
    )
    manufacturer = models.CharField(
        max_length=255,
        verbose_name='Manufacturer',
        db_column='manufacturer',
    )
    manufacturer_number = models.CharField(
        max_length=255,
        verbose_name='Manufacturer Number',
        db_column='manufacturer_number',
    )

    class Meta:
        db_table = 'materials'
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        ordering = ['manufacturer', 'description']

    def __str__(self):
        return f'{self.description} | {self.manufacturer}'


class MaterialVendor(models.Model):
    id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='ID',
        auto_created=True,
        db_column='id',
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name='Material',
        db_column='material_id',
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        verbose_name='Vendor',
        db_column='vendor_id',
    )
    vendor_description = models.CharField(
        max_length=255,
        verbose_name='Vendor Description',
        db_column='vendor_description',
    )
    vendor_part_number = models.CharField(
        max_length=255,
        verbose_name='Vendor Part Number',
        db_column='vendor_part_number',
    )
    vendor_unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Vendor Unit Price',
        db_column='vendor_unit_price',
    )
    vendor_unit_of_measure = models.CharField(
        max_length=255,
        verbose_name='Vendor Unit of Measure',
        db_column='vendor_unit_of_measure',
    )
    vendor_product_link = models.URLField(
        max_length=255,
        verbose_name='Vendor Product Link',
        db_column='vendor_product_link',
        blank=True,
        null=True,
    )
    vendor_image_link = models.URLField(
        max_length=255,
        verbose_name='Vendor Image Link',
        db_column='vendor_image_link',
        blank=True,
        null=True,
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Modified',
        db_column='last_modified',
        blank=True,
        null=True,
    )
    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Last Modified By',
        db_column='last_modified_by',
    )

    class Meta:
        db_table = 'material_vendors'
        verbose_name = 'Material Vendor'
        verbose_name_plural = 'Material Vendors'
        ordering = ['vendor', 'material']
        unique_together = ('material', 'vendor')

    def __str__(self):
        return f'{self.vendor} | {self.material}'

    def save(self, *args, **kwargs):
        self.vendor_description = self.vendor_description.lower()
        self.vendor_part_number = self.vendor_part_number.lower()
        self.vendor_unit_of_measure = self.vendor_unit_of_measure.lower()
        super(MaterialVendor, self).save(*args, **kwargs)
