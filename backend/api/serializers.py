from rest_framework import serializers
from .models import BotUser

class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = ["id", "user_id", "username", "full_name",
                  "phone_number", "twofa_password",
                  "dayly_limit", "language_code"]
        extra_kwargs = {
            "twofa_password": {"write_only": True,
                               "required": False,
                               "allow_null": True,
                               "allow_blank": True}
        }

class SendMessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    message_id = serializers.CharField(required=False)
    from_chat_id = serializers.CharField(required=False)
