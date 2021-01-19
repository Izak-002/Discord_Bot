import discord
import os
import random
import giphy_client
from giphy_client.rest import ApiException
from dotenv import load_dotenv
import requests
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
giphy_api_key = os.getenv('GIPHY_KEY')
bot = discord.Client()

# ---------------------------------------------------
intents = discord.Intents.all()
# bot = discord.Client(intents=intents)
# ---------------------------------------------------

# api stuff------------------------------------------
api_instance = giphy_client.DefaultApi()

# ----------------------------------------------------

# make bot prefix-------------------------------------
from discord.ext import commands
help_category = commands.DefaultHelpCommand(no_category='Commands of Bot')
bot = commands.Bot(command_prefix='$',
                   help_command=help_category,
                   intents=intents)

# ----------------------------------------------------


# search funtion for gifs
def search_gifs(query):

    try:
        return api_instance.gifs_search_get(giphy_api_key,
                                            query,
                                            limit=6,
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


# this is to get the quote
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' - said by ' + json_data[0]['a']
    return quote


@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user))


@bot.event
async def on_message(message):

    await bot.process_commands(message)

    if message.author == bot.user:
        return

    bad_words = ['bad', 'test', 'anime']

    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send(f"How dare you hurt rikka's feelings")

    if message.content.lower().startswith('im'):
        await message.channel.send(f'hey{message.content[2:]} Im dad ^-^')

    if message.content.startswith('uwu'):
        await message.channel.send('ara ara onii-chan')
        await message.channel.send(gif_response('anime'))

    #         f'{message.author.mention} pats {message.mentions[0].mention}\n')


# bot commands---------------------------------------

# @bot.command(
# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
# help=
# "Uses come crazy logic to determine if pong is actually the correct value or not.",
# ADDS THIS VALUE TO THE $HELP MESSAGE.
# brief="Prints pong back to the channel.")
# async def ping(ctx):
# SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
# await ctx.channel.send("pong")


@bot.command(help='Just use $rikka to activate command',
             brief='When command is used it shows random gif of rikka')
async def rikka(ctx):

    await ctx.channel.send(gif_response('rikka'))


@bot.command(
    help='use $pat and someones username to actiavte command e.g. [$pat @jack]',
    brief='when used it wil send a headpat gif to someone ^-^')
async def pat(ctx, user: discord.Member):

    gifs = api_instance.gifs_search_get(giphy_api_key,
                                        'anime pat',
                                        limit=6,
                                        rating='g')
    gif = gifs.data[1]
    await ctx.channel.send(f'{ctx.author.name} pats {user.mention}\n')
    await ctx.channel.send(gif.url)


@bot.command(
    help='use $hug and someones username to activate command e.g. [$hug @jack]',
    brief='When used it wil send a hug gif to someone :)')
async def hug(ctx, user: discord.Member):

    gifs = api_instance.gifs_search_get(giphy_api_key,
                                        'Anime hug',
                                        limit=50,
                                        rating='g')
    gif = gifs.data[16]
    await ctx.channel.send(f'{ctx.author.name} hugs {user.mention}\n')
    await ctx.channel.send(gif.url)


@bot.command(help='use $wise to get random quote',
             brief='When used it will show a random quote')
async def wise(ctx):

    quote = get_quote()
    await ctx.channel.send(quote)


# -----------------------------------------------------


@bot.event
async def on_member_join(member):

    await member.create_dm()

    await member.dm_channel.send(
        f'Yahallo {member.name} Welcome to the server\n')

    role = discord.utils.get(member.guild.roles, name="Nani?")
    await member.add_roles(role, reason=None, atomic=True)

    gifs = api_instance.gifs_search_get(giphy_api_key, 'loli', rating='g')
    gif = gifs.data[1]
    await member.dm_channel.send(gif.url)

    for channel in member.guild.channels:
        if str(channel) == 'general':
            await channel.send(f'Welcome {member.mention} to the server ^-^')


bot.run(TOKEN)