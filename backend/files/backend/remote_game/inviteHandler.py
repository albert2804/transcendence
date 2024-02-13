import asyncio
from .gameHandler import GameHandler
from channels.layers import get_channel_layer

class InviteHandler:
    all_invitations = {}

    def __init__(self, inviter, invitee, accepted=False):
        self.inviter = inviter
        self.invitee = invitee
		self.accepted = accepted
        self.invitation_group = f"invitation_{random.randint(0, 1000000)}"
        InviteHandler.all_invitations[self.invitation_group] = self
        self.channel_layer = get_channel_layer()
		self.chat_consumer = ChatConsumer()
		self.game_group = None
	
	async def invite()
		if accepted:
			print("Invite already accepted.")
			return
		# send invitation to invitee
		await chat_consumer.save_and_send_message(self.invitee, self.inviter, 'You have been invited to a game.', datetime.now(), 'info')

	@classmethod
	async def get_all_inviters() # need to add cls as parameter ??
		inviters = []
		for i in cls.all_invitations.values():
			inviters.append(i.inviter)
		return inviters
	
	@classmethod
	async def accept(cls, invitee)
		# find invitation
		# TODO: need to check if there is still an invitation for the i
		invitation = None
		for i in cls.all_invitations.values():
			if i.invitee == invitee:
				invitation = i
				break
		if invitation == None:
			print("No invitation found.")
			return
		# accept invitation
		invitation.accepted = True
		# create game
		self.game_group = await GameHandler.create(self.inviter, self.invitee)

    