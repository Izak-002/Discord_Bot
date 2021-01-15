import discord
import os
import random
import giphy_client
from giphy_client.rest import ApiException
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
giphy_api_key = os.getenv('GIPHY_KEY')
client = discord.Client()

# ---------------------------------------------------
intents = discord.Intents.all()
client = discord.Client(intents=intents)
# ---------------------------------------------------

# api stuff------------------------------------------
api_instance = giphy_client.DefaultApi()

# ----------------------------------------------------


# search funtion for gifs
def search_gifs(query):

    try:
        return api_instance.gifs_search_get(giphy_api_key, query, rating='g')

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


@client.event
async def on_ready():
    print('We have logged in as {}'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('uwu'):
        await message.channel.send('ara ara onii-chan')


@client.event
async def on_member_join(member):

    await member.create_dm()

    await member.dm_channel.send(
        f'Yahallo {member.name} Welcome to the server\n')

    role = discord.utils.get(member.guild.roles, name="Nani?")
    await member.add_roles(role, reason=None, atomic=True)


client.run(TOKEN)