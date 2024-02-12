import asyncio
from .gameHandler import GameHandler
from channels.layers import get_channel_layer

class InviteHandler:
    all_invitations = {}

    def __init__(self, inviter, invitee):
        self.inviter = inviter
        self.invitee = invitee
        self.invitation_group = f"invitation_{random.randint(0, 1000000)}"
        InviteHandler.all_invitations[self.invitation_group] = self
        self.channel_layer = get_channel_layer()
    
    