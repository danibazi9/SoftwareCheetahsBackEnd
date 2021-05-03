from django.db import models
from account.models import Account

class Chat(models.Model):
    account1 = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='account1')
    account2 = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='account2')

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    parentMessage = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(db_index=True)

