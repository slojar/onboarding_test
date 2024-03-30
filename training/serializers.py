from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import APIException

from training.models import Activity, UserActivity, UserActivityLog, do_training


class ActivitySerializerOut(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = []


class UserActivityLogSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        exclude = []
        depth = 1


class UserSerializerOut(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password", "last_login", "is_superuser", "first_name", "last_name", "email", "is_staff", "date_joined",
            "groups", "user_permissions"
        ]


class EnterAppSerializerIn(serializers.Serializer):
    username = serializers.CharField()

    def create(self, validated_data):
        username = str(validated_data.get("username")).lower()

        # Get or Create user
        user_obj, created = User.objects.get_or_create(username=username)
        return UserSerializerOut(user_obj).data


class PerformActivitySerializerIn(serializers.Serializer):
    activity_id = serializers.IntegerField()
    username = serializers.CharField()

    def create(self, validated_data):
        activity_id = validated_data.get("activity_id")
        username = str(validated_data.get("username")).lower()

        activity = get_object_or_404(Activity, id=activity_id)
        user = get_object_or_404(User, username=username)

        # Create user activity
        u_activity = UserActivity.objects.create(user=user, activity=activity)

        # Generate Score for activity log
        training_score = do_training()
        activity_log = UserActivityLog.objects.create(user_activity=u_activity, score=training_score)
        return UserActivityLogSerializerOut(activity_log).data


class InvalidRequestException(APIException):
    status_code = 400
    default_detail = 'Invalid request'
    default_code = 'invalid_request'


def raise_serializer_error_msg(errors: {}):
    message = ""
    for err_key, err_val in errors.items():
        if type(err_val) is list:
            err_msg = ', '.join(err_val)
            message = f'Error occurred on \'{err_key.replace("_", " ")}\' field: {err_msg}'
        else:
            for err_val_key, err_val_val in err_val.items():
                err_msg = ', '.join(err_val_val)
                message = f'Error occurred on \'{err_val_key}\' field: {err_msg}'
                # msg = f'Error occurred on \'{err_val_key.replace("_", " ")}\' field: {err_msg}'
        raise InvalidRequestException(message)

