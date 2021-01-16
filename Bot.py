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
        return api_instance.gifs_search_get(giphy_api_key,
                                            query,
                                            limit=5,
                                            rating='g')

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


# this is the response with gif function
def gif_response(input):

    gifs = search_gifs(input)
    lst = list(gifs.data)
    gif = random.choice(lst)

    # gif = gifs.data[5]
    return gif.url


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
        await message.channel.send(gif_response('anime'))

    if message.content.startswith('$rikka'):
        await message.channel.send(gif_response('rikka'))

    # help for commands-------------------------------
    if message.content.startswith('$help'):
        await message.channel.send('the following commands are available: \n'
                                   'uwu  --- returns a random anime gif ^-^ \n'
                                   '$rikka  --- returns a random rikka gif ^-^'
                                   )


@client.event
async def on_member_join(member):

    await member.create_dm()

    await member.dm_channel.send(
        f'Yahallo {member.name} Welcome to the server\n')

    role = discord.utils.get(member.guild.roles, name="Nani?")
    await member.add_roles(role, reason=None, atomic=True)

    gifs = api_instance.gifs_search_get(giphy_api_key, 'loli', rating='g')
    gif = gifs.data[2]
    await member.dm_channel.send(gif.url)

    for channel in member.guild.channels:
        if str(channel) == 'general':
            await channel.send(f'Welcome the new weirdo {member.mention} ^-^')


client.run(TOKEN)