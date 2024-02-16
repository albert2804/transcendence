from django.db import models
from django.contrib.auth import get_user_model


# If the subtype is 'msg':
# The message is a chat message from one user to another.
#
# If the subtype is 'info':
# The message is an info message from the server to receiver.
# In this case the message should not be sent to the sender.
# The "sender"-field is used to store the chat_id, in which the info message should be shown to the receiver.

class ChatMessage(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)
    subtype = models.CharField(max_length=100, default='msg')

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.created_at}'