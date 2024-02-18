from django.contrib import admin
from .models import Note, SharedNote, NoteUpdateHistory

admin.site.register(Note)
admin.site.register(SharedNote)
admin.site.register(NoteUpdateHistory)
