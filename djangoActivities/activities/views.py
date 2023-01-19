from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ActivitySerializer
from .models import Activity
from .user.models import User
from urllib.request import urlopen
import json
from .constants import ACTIVITIES_URL


class EventView(APIView):
    def post(self, request):
        response = urlopen(ACTIVITIES_URL)
        es = ActivitySerializer(data=json.loads(response.read()))
        if es.is_valid():
            if hasattr(self.request, 'user'):
                es.save(user=self.request.user)
            else:
                user = User.objects.update_or_create()
                es.save(user=user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(data=es.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        activities = Activity.objects.filter(user=self.request.user).all()
        return Response({"Activities": activities})

    def update(self, request):
        activity = Activity.objects.filter(key=self.request.key)
        activity.update(done=True if not activity.done else False)
        return Response(status=status.HTTP_200_OK)
