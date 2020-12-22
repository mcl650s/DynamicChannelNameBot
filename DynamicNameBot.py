import os

import discord
import asyncio

from dotenv import load_dotenv
from collections import Counter

intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.check_game_update())

    async def on_ready(self):
        print('--------------------------------------------------')
        print(f'Logged in as: {self.user.name} {self.user.id}')
        print('--------------------------------------------------')

    async def check_game_update(self):
        await self.wait_until_ready()
        activityList = []
        while not self.is_closed():
            for guild in self.guilds:
                for channel in guild.voice_channels:
                    if(len(channel.members) > 0):
                        for chatter in channel.members:
                            if(chatter.activity != None and chatter.activity.type.name == 'playing'):
                                activityList.append(chatter.activity.name)
                            else:
                                activityList.append('Just Chatting')
                        new_name = str(Counter(activityList).most_common(1)[0][0])
                        #await channel.edit(name=new_name) #Can only send 2 changes per 10 minutes? So do it every 5 I think
                        channel2 = self.get_channel(789229582292746253)
                        await channel2.send(new_name)
                        activityList.clear()
                await asyncio.sleep(5) # task runs every 5 Minutes, temp set to 5 seconds when sending messages instead of updating channel name


client = MyClient(intents = intents)
client.run(TOKEN)