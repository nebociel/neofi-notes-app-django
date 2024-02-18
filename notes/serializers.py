from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, NoteUpdateHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'owner', 'title',
                  'content', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Note title cannot be empty")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Note content cannot be empty")
        return value


class NoteUpdateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteUpdateHistory
        fields = '__all__'
