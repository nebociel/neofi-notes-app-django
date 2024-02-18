from django.urls import path

from .views import (create_note, delete_note, get_note_version_history, login,
                    note_detail, share_note, signup)

urlpatterns = [
    path('signup/', signup),
    path('login/', login),
    path('notes/create/', create_note),
    path('notes/share/', share_note),
    path('notes/<int:id>/', note_detail),
    path('notes/version-history/<int:id>/', get_note_version_history),
    path('notes/delete/<int:id>/', delete_note),
]
