from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from training.models import UserActivityLog, Activity
from training.serializers import EnterAppSerializerIn, raise_serializer_error_msg, PerformActivitySerializerIn, \
    ActivitySerializerOut


class UserEnterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = EnterAppSerializerIn(data=request.data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        response = serializer.save()
        return Response({"message": "Welcome", "data": response})


class LeadersBoardAPIView(APIView):
    permission_classes = []

    def get(self, request):
        # Return Leaders Board
        users = User.objects.all().exclude(is_staff=True)
        result = [{
            "username": user.username,
            "score": UserActivityLog.objects.filter(user_activity__user=user).aggregate(Sum("score"))["score__sum"] or 0
        } for user in users]
        response = sorted(result, key=lambda x: x['score'], reverse=True)

        return Response({"message": "Success", "deta": response})


class PerformActivityAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PerformActivitySerializerIn(data=request.data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        response = serializer.save()
        return Response({"message": "Success", "data": response})


class ActivitiesListAPIView(ListAPIView):
    permission_classes = []
    serializer_class = ActivitySerializerOut
    queryset = Activity.objects.all()


