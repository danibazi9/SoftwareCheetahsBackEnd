from rest_framework import serializers
from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):
    ctime = serializers.SerializerMethodField('get_ctime')

    class Meta:
        model = Message
        fields = ['message_id', 'chat', 'owner', 'text' , 'parrent_message', 'get_ctime']

    def get_ctime(self, message):
        return message.time.ctime()
