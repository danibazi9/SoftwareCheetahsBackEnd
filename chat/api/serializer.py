from rest_framework import serializers
from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):
    ctime = serializers.SerializerMethodField('get_ctime')

    class Meta:
        model = Message
        fields = ['message_id', 'chat', 'owner', 'text' , 'parent_message', 'ctime']

    def get_ctime(self, message):
        return message.time.ctime()
