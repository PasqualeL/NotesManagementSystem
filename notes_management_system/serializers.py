from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(),required=False,default=list,)#necessario perchè se no in swagger appaiono le {} anzichè le []
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())#controllo del currentUser per modificare solo note dell'user che le crea

    class Meta:
        model = Note
        fields = ["id", "title", "content", "tags", "created_at", "updated_at","owner"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_tags(self, value):
        norm_tags = {str(v).strip().lower() for v in value if str(v).strip()}#normalizza: stringhe, trim, lowercase, uniche
        return sorted(norm_tags)
