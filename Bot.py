import discord
import os
import random
import giphy_client
from giphy_client.rest import ApiException
from dotenv import load_dotenv
import requests
import json
from mal import *

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

# gets anime quote
def get_anime_quote():
    response = requests.get('https://animechanapi.xyz/api/quotes/random')
    json_data = json.loads(response.text)
    # data = json_data['data'][0]['quote']
    quote = json_data['data'][0]['quote'] + ' - said by ' + json_data['data'][0]['character'] + ' - ' + json_data['data'][0]['anime']
    return quote







# --------------------------------------------------------------------
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


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandInvokeError):
#         await ctx.channel.send(str(error.original))




# bot commands---------------------------------------

@bot.command(help='Just use $rikka to activate command',
             brief='shows random gif of rikka')
async def rikka(ctx):

    await ctx.channel.send(gif_response('rikka'))


@bot.command(
    help='use $pat and someones username to actiavte command e.g. [$pat @jack]',
    brief='send a headpat gif to someone ^-^')
async def pat(ctx, user: discord.Member):


    embed = discord.Embed(description=f'**{ctx.author.name}** pats {user.mention}',
                          color=0x00ffdd)

    gifs = [
        'https://media.giphy.com/media/4HP0ddZnNVvKU/giphy.gif',
        'https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif',
        'https://media.giphy.com/media/109ltuoSQT212w/giphy.gif',
        'https://media.giphy.com/media/L2z7dnOduqEow/giphy.gif'
    ]

    gif = random.choice(gifs)
    embed.set_image(url=gif)

    
    await ctx.channel.send(embed=embed)


@bot.command(
    help='use $hug and someones username to activate command e.g. [$hug @jack]',
    brief='send a hug gif to someone :)')
async def hug(ctx, user: discord.Member):

    embed = discord.Embed(description=f'**{ctx.author.name}** hugs {user.mention}',
                          color=0x00ffdd)
    gifs = [
        'https://media.giphy.com/media/3bqtLDeiDtwhq/giphy.gif',
        'https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif',
        'https://media.giphy.com/media/ZQN9jsRWp1M76/giphy.gif'
    ]
  
    gif = random.choice(gifs)
    embed.set_image(url=gif)

    # await ctx.channel.send(f'{ctx.author.name} hugs {user.mention}\n')
    await ctx.channel.send(embed=embed)





@bot.command(help='use $wise to get random quote', brief='show a random quote')
async def wise(ctx):

    quote = get_quote()
    await ctx.channel.send(quote)




@bot.command(help='use $aq to get a random anime quote',
             brief='show a random anime quote')
async def aq(ctx):

    quote = get_anime_quote()
    await ctx.channel.send(quote)




@bot.command(help='use $alist to show anime options e.g. $alist rezero',
             brief='show names and ID of anime')
async def alist(ctx):
    anime_search = ctx.message.content[7:]
    anime = AnimeSearch(anime_search)
    anime_results = anime.results[:7]
    anime_results2 = anime.results[7:14]
    results = ''
    results2 = ''
    for anime in anime_results:
        results = results  + '**[' + str(
            anime.mal_id) + ']**' + anime.title + '\n'

    for anime in anime_results2:
        results2 = results2 + '**[' + str(
            anime.mal_id) + ']**' + anime.title + '\n'
        # await ctx.channel.send(anime.title)

    # anime_id = anime.results.mal_id
    # await ctx.channel.send(
    #     results + '\n' +
    #     'Tip use the numbers after title to use the $info command')



    page1 = discord.Embed (
        title = 'Page 1/2',
        description = 'To see info on an anime use ```$info and the anime ID```' + '\n' + results + '\n',
        colour = discord.Colour.green()
    )

    # page1.add_field(name='```Help```', value='use $info and the anime ID to get more info on anime', inline=False)

    page2 = discord.Embed (
        title = 'Page 2/2',
        description = 'To see info on an anime use ```$info and the anime ID```' + '\n' + results2 + '\n',
        colour = discord.Colour.green()
    )
    
    pages = [page1, page2]

    message = await ctx.send(embed = page1)
    await message.add_reaction('◀')
    await message.add_reaction('▶')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', check = check)
            await message.remove_reaction(reaction, user)

            if str(reaction) == '▶':
                if i < 1:
                    i += 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])

        except:
            break


@bot.command()
async def info(ctx):
    anime_id = ctx.message.content[6:]
    anime = Anime(anime_id)
    # anime_search = ctx.message.content[6:]
    # anime_result = AnimeSearch(anime_search)
    # results = anime_result.results[1]
    # anime_id = results.mal_id
    # anime = Anime(anime_id)

    # await ctx.channel.send(anime.title + '\n' + anime.synopsis + '\n' +
    #                        str(anime.popularity) + '\n' + str(anime.rank) +
    #                        '\n' + ' '.join(anime.genres))
    embed = discord.Embed(title=anime.title,
                          description=anime.synopsis + '\n' + '\n' +
                          'Genres: ' + ' ,'.join(anime.genres),
                          color=0x00ffdd)
    # embed.set_image(url=ctx.author.avatar_url)
    embed.set_thumbnail(url=anime.image_url)

    embed.set_author(name=ctx.author.display_name +
                     ' requested info on an anime',
                     icon_url=ctx.author.avatar_url)

    embed.add_field(name='Popularity',
                    value=str(anime.popularity),
                    inline=True)

    embed.add_field(name='Anime Rank', value=str(anime.rank), inline=True)

    embed.add_field(name='Episodes', value=str(anime.episodes), inline=False)

    embed.set_footer(text='Studios ' + ','.join(anime.studios) + '\nType: ' +
                     anime.type)

    await ctx.channel.send(embed=embed)


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

    num_of_bots = 0
    members = member.guild.members
    for m in members:
        if m.bot:
            num_of_bots = num_of_bots + 1
    member_count = member.guild.member_count
    total_members = member_count - num_of_bots

    for channel in member.guild.channels:
        if str(channel) == 'general':
            await channel.send(f'Welcome {member.mention} to the server ^-^ ' + f'You are now one of the {str(total_members)} members of the server')


bot.run(TOKEN)