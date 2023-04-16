from django.db import models


class Equipment(models.Model):
    equipment_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Equipment ID',
        db_column='equipment_id',
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Description',
        db_column='description',
    )

    class Meta:
        db_table = 'equipment'
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        ordering = ['equipment_id']

    def __str__(self):
        return self.description
