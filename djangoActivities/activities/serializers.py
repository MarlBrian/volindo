from rest_framework.serializers import ModelSerializer
from .models import Activity


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'user', 'name', 'type', 'participants', 'price',
            'link', 'key', 'accessibility', 'done'
        )
        exclude = ['user', 'done']
