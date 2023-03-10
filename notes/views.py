from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from notes.models import Note
from notes.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from notes.serializers import NoteSerializer


class NoteAPIList(generics.ListCreateAPIView):
    """
    Вид для создания новой записи или просмотра всего списка записей Note
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    authentication_classes = (TokenAuthentication,)


class NoteAPIUpdate(generics.RetrieveUpdateAPIView):
    """
    Вид для изменения записей Note
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    # authentication_classes = (TokenAuthentication, )


class NoteAPIDestroy(generics.RetrieveDestroyAPIView):
    """
    Вид для удаления записей Note
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsOwnerOrReadOnly, )
