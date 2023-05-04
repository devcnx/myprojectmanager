""" 
Notes Admin Configurations. 
"""

from django.contrib import admin
from .models import Note 


class NoteAdmin(admin.ModelAdmin):
    list_display = ('note_id', 'note', 'author', 'created_on') # The fields that will be displayed on the admin page. 
    list_display_links = ('note_id', 'note') # The fields that will be linked to the detail page.
    list_filter = ('author', 'created_on') # Filter options that will be displayed on the right side of the admin page.
    search_fields = ('note', 'author__first_name', 'author__last_name') # The fields that will be searched when the user searches for a note.
    list_per_page = 50 # The number of notes that will be displayed on each page.
    ordering = ['-created_on'] # Sort the notes by the date they were created on, with the most recent notes at the top.


admin.site.register(Note, NoteAdmin)
