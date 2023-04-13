from django.contrib.auth.models import User 
from django.db import models


class Note(models.Model):
    note_id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='Note ID',
        db_column='note_id',
    )
    note = models.TextField(
        verbose_name='Note',
        db_column='note',
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Author',
        db_column='author',
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        db_column='created_on',
    )

    class Meta:
        db_table = 'notes'
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-created_on']

    def __str__(self):
        return self.note 
    
    def save(self, *args, **kwargs):
        if not self.note_id:
            note_count = Note.objects.count()
            if note_count == 0:
                self.note_id = 1
            else:
                self.note_id = Note.objects.last().note_id + 1
        return super().save(*args, **kwargs)