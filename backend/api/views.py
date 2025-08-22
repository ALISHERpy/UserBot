from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import time
from core import settings
from .models import BotUser
from .serializers import BotUserSerializer, SendMessageSerializer
import requests

class CreateOrUpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create new user or update existing by `user_id`.
        Only updates fields explicitly provided (not overwriting with null).
        """
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = BotUser.objects.filter(user_id=user_id).first()

        # Yangi foydalanuvchi yaratish
        if not user:
            serializer = BotUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Mavjud foydalanuvchini update qilish: faqat request.data dagi maydonlar
        update_data = {}
        for field in BotUserSerializer.Meta.fields:
            if field in request.data and request.data[field] not in (None, ""):
                update_data[field] = request.data[field]

        serializer = BotUserSerializer(user, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendMessageSerializer

    def post(self, request):
        BOT_TOKEN = settings.BOT_TOKEN
        base = f"https://api.telegram.org/bot{BOT_TOKEN}"

        message_id = request.data.get("message_id")
        from_chat_id = request.data.get("from_chat_id")
        text = request.data.get("text")

        if message_id:
            # Copy an existing message
            url = f"{base}/copyMessage"
            payload = {
                "from_chat_id": from_chat_id,   # must be included!
                "message_id": message_id,
            }
        elif text:
            url = f"{base}/sendMessage"
            payload = {
                "text": text
            }
        else:
            return Response(
                {"error": "Either text or message_id must be provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        telegram_ids = BotUser.objects.all().values_list("user_id", flat=True)
        for telegram_id in telegram_ids:
            try:
                payload["chat_id"] = telegram_id
                resp = requests.post(url, json=payload)
            except Exception as e:
                pass
            time.sleep(0.3)
        return Response(resp.json(), status=status.HTTP_200_OK)


