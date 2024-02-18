from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class NoteUpdateHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    old_title = models.CharField(max_length=255)
    old_content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:  # If creating a new instance
            if self.note_id:
                self.old_title = self.note.title
                self.old_content = self.note.content
        super().save(*args, **kwargs)
