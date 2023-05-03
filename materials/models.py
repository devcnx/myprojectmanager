from datetime import datetime
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
        unique=True,
    )

    class Meta:
        db_table = 'materials'
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        ordering = ['description', 'manufacturer']

    def __str__(self):
        return f'{self.description} | {self.manufacturer}'

    def get_unique_manufacturers():
        # Only return unique manufacturers
        # Convert all manufacturers to lowercase
        # Sort the list
        # Return the list
        return sorted(set([x.manufacturer.lower() for x in Material.objects.all()]))


class MaterialAlternativeManufacturerNumber(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE,
        verbose_name='Material',
        related_name='material_alternatives',
        db_column='material_id',
    )
    alternative_manufacturer_number = models.CharField(
        max_length=255,
        verbose_name='Alternative Manufacturer Number',
        db_column='alternative_manufacturer_number',
        unique=True,
    )

    class Meta:
        db_table = 'material_alt_mfr_numbers'
        verbose_name = 'Material Alternative Manufacturer Number'
        verbose_name_plural = 'Material Alternative Manufacturer Numbers'
        ordering = ['material', 'alternative_manufacturer_number']

    def __str__(self):
        return f'{self.material.description} | {self.alternative_manufacturer_number}'


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
        limit_choices_to={'vendor_type': 1},
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
        related_name='last_modified_by',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'material_vendors'
        verbose_name = 'Material Vendor'
        verbose_name_plural = 'Material Vendors'
        ordering = ['vendor', 'material']
        # unique_together = ('material', 'vendor')

    def __str__(self):
        return f'{self.vendor} | {self.material}'

    def save(self, *args, **kwargs):
        self.last_modified = datetime.now()
        self.last_modified_by = User.objects.get(username='automations')
        super(MaterialVendor, self).save(*args, **kwargs)


class MaterialOrder(models.Model):
    material_order_id = models.AutoField(
        primary_key=True,
        verbose_name='Material Order ID',
        db_column='material_order_id',
        editable=False,
    )
    material_order_date = models.DateField(
        verbose_name='Material Order Date',
        db_column='material_order_date',
    )
    material_order_vendor = models.ForeignKey(
        Vendor,
        verbose_name='Material Order Vendor',
        db_column='material_order_vendor',
        related_name='material_order_vendor',
        on_delete=models.CASCADE,
        limit_choices_to={'vendor_type': 1},
    )
    material_order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Material Order Total',
        db_column='material_order_total',
        default=0.00,
    )
    material_order_notes = models.TextField(
        verbose_name='Material Order Notes',
        db_column='material_order_notes',
        blank=True,
        null=True,
    )
    material_order_created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Material Order Created By',
        db_column='material_order_created_by',
        related_name='material_order_created_by',
    )
    material_order_last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Material Order Last Modified',
        db_column='material_order_last_modified',
        blank=True,
        null=True,
    )
    material_order_last_modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Material Order Last Modified By',
        db_column='material_order_last_modified_by',
        related_name='material_order_last_modified_by',
    )

    class Meta:
        db_table = 'material_orders'
        verbose_name = 'Material Order'
        verbose_name_plural = 'Material Orders'
        ordering = ['material_order_date', 'material_order_vendor']

    def __str__(self):
        return f'{self.material_order_vendor} | {self.material_order_date}'

    def save(self, *args, **kwargs):
        super(MaterialOrder, self).save(*args, **kwargs)


class MaterialOrderItem(models.Model):
    order_item_id = models.AutoField(
        primary_key=True,
        verbose_name='Order Item ID',
        db_column='order_item_id',
        editable=False,
    )
    material_order = models.ForeignKey(
        MaterialOrder,
        verbose_name='Material Order',
        db_column='material_order',
        related_name='material_order',
        on_delete=models.CASCADE,
        null=True,
    )
    material_order_item = models.ForeignKey(
        Material,
        verbose_name='Order Item',
        db_column='material_order_item',
        related_name='material_order_item',
        on_delete=models.CASCADE,
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Quantity',
        db_column='quantity',
    )
    unit_of_measure = models.CharField(
        max_length=255,
        verbose_name='Unit of Measure',
        db_column='unit_of_measure',
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Unit Price',
        db_column='unit_price',
    )

    class Meta:
        db_table = 'material_order_items'
        verbose_name = 'Material Order Item'
        verbose_name_plural = 'Material Order Items'
        ordering = ['material_order_item', 'quantity', 'unit_of_measure']

    def __str__(self):
        return f'{self.material_order_item} | {self.quantity} {self.unit_of_measure}'
