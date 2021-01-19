import discord
import asyncio

from dotenv import load_dotenv
from collections import Counter
from os import getenv


intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.check_game_update())

    async def on_ready(self):
        print('--------------------------------------------------')
        print(f'Logged in as: {self.user.name} {self.user.id}')
        print('--------------------------------------------------')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Game Activity"))

    async def check_game_update(self):
        await self.wait_until_ready()
        while not self.is_closed():
            for guild in self.guilds:
                for channel in guild.voice_channels:
                    if(len(channel.members) > 0):
                        numChatting = 0
                        vidChatting = 0
                        activityList = []
                        for chatter in channel.members:
                            if(chatter.activity == None):
                                numChatting += 1
                                if(chatter.voice.self_video):
                                    vidChatting += 1
                            elif(chatter.activity.type.name == 'playing' or chatter.activity.type.name == 'streaming'):
                                activityList.append(chatter.activity.name)
                            else:
                                numChatting += 1
                                if(chatter.voice.self_video):
                                    vidChatting += 1

                        if(numChatting > (len(channel.members)/2)):
                            if(vidChatting > (numChatting/2)):
                                new_name = 'Garage Talk'
                            else:
                                new_name = 'Just Chatting'
                        else:
                            new_name = str(Counter(activityList).most_common(1)[0][0])
                        await channel.edit(name=new_name)
                        channel2 = self.get_channel(791066555085094923)
                        await channel2.send(new_name)
                await asyncio.sleep(300) # task runs every 5 Minutes, temp set to 5 seconds when sending messages instead of updating channel name

client = MyClient(intents = intents)
client.run(TOKEN)