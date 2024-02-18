from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Note, NoteUpdateHistory, SharedNote
from .serializers import (NoteSerializer, NoteUpdateHistorySerializer,
                          UserSerializer)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password before saving
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password'])
        serializer.save()
        return Response("User registration successful", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response("Both username and password are required", status=status.HTTP_400_BAD_REQUEST)

    # Authenticate user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        return Response({
            'token': token,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    else:
        return Response("Invalid username or password", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response("Note created successfully", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def note_detail(request, id):
    try:
        note = Note.objects.get(id=id)
        if request.method == 'GET':
            if request.user == note.owner or SharedNote.objects.filter(note=note, user=request.user).exists():
                serializer = NoteSerializer(note)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Unauthorized to view this note", status=status.HTTP_403_FORBIDDEN)
        elif request.method == 'PUT':
            if request.user != note.owner and not SharedNote.objects.filter(note=note, user=request.user).exists():
                return Response("Unauthorized to update this note", status=status.HTTP_403_FORBIDDEN)
            serializer = NoteSerializer(instance=note, data=request.data)
            if serializer.is_valid():
                serializer.save()

                # Create NoteUpdateHistory instance
                NoteUpdateHistory.objects.create(
                    note=note,
                    old_title=note.title,
                    old_content=note.content,
                )

                return Response("Note updated successfully", status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Note.DoesNotExist:
        return Response("Note not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    note_id = request.data.get('note_id')
    users = request.data.get('users')
    try:
        note = Note.objects.get(id=note_id, owner=request.user)
        for user_id in users:
            try:
                user = User.objects.get(id=user_id)
                shared_note = SharedNote.objects.create(note=note, user=user)
                shared_note.save()
            except User.DoesNotExist:
                return Response(f"User with ID {user_id} not found", status=status.HTTP_404_NOT_FOUND)
        return Response("Note shared successfully", status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response("Note not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, id):
    try:
        note = Note.objects.get(id=id)
        if request.user == note.owner or SharedNote.objects.filter(note=note, user=request.user).exists():
            version_history = NoteUpdateHistory.objects.filter(note=note)
            serializer = NoteUpdateHistorySerializer(
                version_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Unauthorized to view version history of this note", status=status.HTTP_403_FORBIDDEN)
    except Note.DoesNotExist:
        return Response("Note not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note(request, id):
    try:
        note = Note.objects.get(id=id, owner=request.user)
        note.delete()
        return Response("Note deleted successfully", status=status.HTTP_204_NO_CONTENT)
    except Note.DoesNotExist:
        return Response("Note not found", status=status.HTTP_404_NOT_FOUND)
