from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    authentication_classes = [JWTAuthentication,SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["title", "content"]

    def get_queryset(self):

        qs = Note.objects.filter(owner=self.request.user)
        #?tags=fantasy,sci-fi basta che ne abbia almeno uno
        tags = self.request.query_params.get("tags")
        if not tags:
            return qs
        tags_wanted = [t.strip().lower() for t in tags.split(",") if t.strip()]
        tag_ids = []
        for note in qs:
            note_tags = [t.lower() for t in (note.tags or [])]
            for t in tags_wanted:
                if t in note_tags:
                    tag_ids.append(note.id)
                    break  # ne ha almeno uno
        return qs.filter(pk__in=tag_ids)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)#salva automaticamente l'utente dalla sessione

    #SWAGGER region

    @swagger_auto_schema(
        operation_summary="Notes List",
        tags=["Notes"],
        security=[{"Bearer": []}],
        manual_parameters=[
            openapi.Parameter("search", openapi.IN_QUERY, description="Search in the title or content  for example:meeting, holyday.", type=openapi.TYPE_STRING),
            openapi.Parameter("tags", openapi.IN_QUERY, description="Specific tag filter: tags=urgent,important", type=openapi.TYPE_STRING),
        ],
        responses={200: NoteSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Note",
        tags=["Notes"],
        security=[{"Bearer": []}],
        responses={201: NoteSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Note Detail",
        tags=["Notes"],
        security=[{"Bearer": []}],
        responses={200: NoteSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Note",
        tags=["Notes"],
        security=[{"Bearer": []}],
        responses={200: NoteSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Patch Note",
        tags=["Notes"],
        security=[{"Bearer": []}],
        responses={200: NoteSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Note",
        tags=["Notes"],
        security=[{"Bearer": []}],
        responses={204: "Nota Eliminata"},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    #END SWAGGER region