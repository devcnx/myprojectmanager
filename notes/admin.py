from django.contrib import admin
from .models import Note 


class NoteAdmin(admin.ModelAdmin):
    list_display = ('note_id', 'note', 'author', 'created_on')
    list_display_links = ('note_id', 'note')
    list_filter = ('author', 'created_on')
    search_fields = ('note', 'author__first_name', 'author__last_name')
    list_per_page = 50 
    ordering = ['-created_on']


admin.site.register(Note, NoteAdmin)