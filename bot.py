import os

import discord

from static_handlers import message_handlers


class MainClient(discord.Client):
    async def on_ready(self):
        print("Ready.")

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
    client = MainClient()
    client.run(os.environ.get("DISCORD_TOKEN"))
