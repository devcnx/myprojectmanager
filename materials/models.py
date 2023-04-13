from django.db import models


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
        ordering = ['description']

    def __str__(self):
        return self.description