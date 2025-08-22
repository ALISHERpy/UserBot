from django.urls import path
from .views import CreateOrUpdateUserAPIView,SendMessageAPIView

urlpatterns = [
    path('bot-users/create-update/', CreateOrUpdateUserAPIView.as_view(), name='create-update-user'),
    path('bot-users/send-message/', SendMessageAPIView.as_view(), name='send_msg'),
]
