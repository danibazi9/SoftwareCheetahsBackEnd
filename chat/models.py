from django.db import models
from account.models import Account


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    account1 = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='account1')
    account2 = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='account2')

    def __str__(self):
        return f"Chat {self.chat_id}: {self.account1.__str__()} + {self.account2.__str__()}"


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    parent_message = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.owner.__str__() + ": " + self.text
