import os

import discord

from static_handlers import message_handlers


GREETING_ON_JOIN = False


landing_channel = 'airlock'
channel_ids = {
    'airlock': 768922224626761772
}


class MainClient(discord.Client):
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

        for condition, handler in message_handlers:
            if condition(message.content.lower()):
                await message.channel.send(handler(message.content, message.author.display_name))
                return

        if message.content.startswith("!"):
            print(f"No handler for bot command {message.content} found.")


if __name__ == '__main__':
    # FIXME figure out the exact intents required
    intents = discord.Intents.all()
    intents.presences = False
    client = MainClient(intents=intents)
    client.run(os.environ.get("DISCORD_TOKEN"))
