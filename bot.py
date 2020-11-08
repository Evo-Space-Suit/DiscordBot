import os

import discord


class MainClient(discord.Client):
    async def on_ready(self):
        print("ready.")

    async def on_message(self, message: discord.Message):
        if message.content.startswith("!test"):
            await message.channel.send("Beep boop :robot:")
        if message.content.startswith("!introduce-yourself"):
            await message.channel.send(
                    "Hi ESS @here!\n"
                    "My name is B-Evo, and in the future I hope to perform the following tasks for the team:\n"
                    "1) Provide a test-bed for the personal assistant that'll be integrated in the suit. :robot: :astronaut:\n"
                    "2) Execute familiar bot-commands like provide meeting summaries and GDrive upload notifications. :robot: :page_facing_up:\n"
                    "3) Act as a companion in these dark times. :robot: :hugging:\n"
                    "Stay safe all. :robot: :family:\n")


if __name__ == '__main__':
    client = MainClient()
    client.run(os.environ.get("DISCORD_TOKEN"))
