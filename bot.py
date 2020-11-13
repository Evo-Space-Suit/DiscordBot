import os

import discord

from static_handlers import message_handlers


GREETING_ON_JOIN = False


landing_channel = 'airlock'
channel_ids = {
    'airlock': 768922224626761772,
    'General': 768922224626761773,  # voice chat
}

user_ids = {
    'Adam': 266680529020125185,
}


class MainClient(discord.Client):
    async def play_in_channel(self, channel, audio, send_invitation=True):
        voice: discord.VoiceChannel = self.get_channel(channel_ids[channel])

        try:
            voice_client: discord.VoiceClient = next(filter(lambda vc: vc.channel.id == channel_ids[channel], self.voice_clients))
        except StopIteration:
            voice_client: discord.VoiceClient = await voice.connect()

        if voice_client.is_playing():
            voice_client.stop()
        voice_client.play(audio)

        if send_invitation:
            return await voice.create_invite(max_age=120, temporary=True)

    async def on_ready(self):
        print("Ready.")

    async def on_member_join(self, member: discord.Member):
        if not GREETING_ON_JOIN: return
        await self.get_channel(channel_ids[landing_channel]).send(
                f"Welcome to the Evo Space Suit Team server {member.display_name} :tada:\n"
                "Take a look around and if you have any questions or wish to participate please reach out to any of our friendly staff.\n")

    async def on_message(self, message: discord.Message):
        if message.author.id == self.user.id:
            return

        for condition, handler, *side_effects in message_handlers:
            if condition(message.content.lower()):
                if handler:
                    await message.channel.send(handler(message.content, message.author.display_name))
                for side_effect in side_effects:
                    await side_effect(self, message)
                return

        # TODO show available commands
        if message.content.startswith("!help"):
            await message.channel.send("I'm still being setup and my abilities evolve rapidly :robot:\n"
                                       f"Please refer to <@{user_ids['Adam']}> if you have a question about me.")
        elif message.content.startswith("!"):
            command, *args = message.content[1:].split()
            await message.channel.send(f"Sorry! I don't know how to do '{command}' at this point :confused:")


if __name__ == '__main__':
    # FIXME figure out the exact intents required
    intents = discord.Intents.all()
    intents.presences = False
    client = MainClient(intents=intents)
    client.run(os.environ.get("DISCORD_TOKEN"))
