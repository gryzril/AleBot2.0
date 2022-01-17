from email import message
from http.server import executable
from multiprocessing.connection import wait
from shlex import join
import string
import discord
import os
import logging
import random
import time
from discord import channel
from discord import member
from discord import FFmpegPCMAudio, PCMVolumeTransformer


from discord.channel import VoiceChannel
from discord.ext.commands import cog
#from discord.ext.commands import bot
from discord.flags import Intents
#from discord.player import AudioSource
#from discord import FFmpegPCMAudio

from Text_Repo import aleQuotes
from BTC import get_price
from BTC import requester
from TTS import Text_To_Speech as TTS
from Games import play_bingo as pb
import get_token

import asyncio
import youtube_dl

from discord.ext import commands
from discord.utils import get

#from recording_handler import args_to_filters, get_encoding, vc_required





# Description #
description = "AleBot2.0. a new paradigm of discord bot"
# Intents # 
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


### Logger ###########################################################################
logger = logging.getLogger('discord')   # Instantiate logger
logger.setLevel(logging.INFO)           # Log all
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)              # Handle logging



### bot #######################################################################

### Bot Commands #######################################################################

@bot.command(name='test')
async def test(ctx):
    print("Test")
    await ctx.send("Test positive")




## Helpers ##

# Returns channel - DEFUNCT
def Connect_From_Message(message):
    member = message.author                     # Get user that requested ?play
    channel = member.voice.channel              # Get channel of user that sent request
                       
    return channel

# Bot Booting up #
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

# Basic Text Commands #

# Say hello, return Bruh
@bot.command()
async def hello(ctx):
    await ctx.send('Bruh')
    
# Get ale quote
@bot.command()
async def quote(ctx):
    str = aleQuotes.get_Ale_Quote()
    await ctx.send(str)
    
# Forces AleBot join
@bot.command()
async def join(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()                                 # Async bot join channel
        logger.info("AleBot2.0 has joined voice channel")
    except:
       await ctx.send('You must be in a VC for AleBot2.0 to join')
    
# Forces AleBot leave
@bot.command()
async def kick(ctx):
    if(ctx.guild):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('AleBot2.0 has been booted')
        logger.info("AleBot2.0 has been booted from VC")
    else:                                                   # else print error
        await ctx.send('AleBot isn\'t in a voice chat or never properly joined')
        logger.info("Failed to boot AleBot2.0")

@bot.command()
async def pick(ctx):
    members = ctx.guild.members
    mem = []
    for item in members:
        mem.append(item.name)
    logger.info("Picking a person in the server...")
    rand = random.randint(0,len(mem)-1)
    str = mem[rand]
    print("Picked",str)
    usr = ctx.guild.get_member(members[rand].id)
    str = "Hey {0.mention}, you have been selected".format(usr)
    print(members)
    await ctx.send(str)
    
@bot.command()
async def clear(ctx, amount = None):
    if int(amount) == None:
        await ctx.channel.purge(limit = 1000000)
    else:
        try:
            int(amount)
        except:
            await ctx.send('Invalid amount')
        else:
            await ctx.channel.purge(limit=int(amount))
    

### BTC #######################################################################################

@bot.command()
async def BTC(ctx):
    """Get Current BTC Price"""
    str = "1 BTC = " + get_price.get_price()
    await ctx.send(str)

@bot.command()
async def set_balance(ctx, id, amount, key):
    if(key != "Admin0147"):
        return await ctx.send("Invalid Key")
    
    requester.set_balance(id, amount)

@bot.command()
async def balance(ctx):
    """Get your BTC Balance"""
    print(ctx.author.name + " " + str(ctx.author.id) + " requesting balance")
    balance = requester.get_balance(str(ctx.author.id))
    strng = ctx.author.name
    await ctx.send(strng + ", your balance is: " + str(balance))
    
@bot.command()
async def all_balances(ctx):
    """Get Balances of all Users"""
    await ctx.send(requester.get_all_balances())

@bot.command()
async def transfer(ctx, username: str, amount: float):
    """Transfer BTC to another user [Username, amount]"""
    id = ctx.author.id
    members = ctx.guild.members
    mem = {}
    for item in members:
        mem[item.name] = item.id
    print(mem)
    
    if(not username in mem):
        return await ctx.send("User not found, try again")
    
    userID = mem[username]
        
    strng = requester.transfer(id, userID, amount)
    await ctx.send(strng)
    
def generate_mine():
    num1 = random.randint(1, 999)
    num2 = random.randint(1, 999)
    sum = num1 + num2
    strng = str(num1) + " + " + str(num2) + " = ?"
    ret = (strng, sum)
    return ret
    
    
    
@bot.command()
async def mine(ctx, iter: int):
    """Mine BTC [Times to Mine]"""
    try:
        int(iter)
    except:
        return await ctx.send("Please enter number of times to mine <1-10>'}")
    
    if(int(iter) > 10):
        return await ctx.send("You can't mine that much, you'll destroy the economy")
    
    if(int(iter) < 1):
        return await ctx.send("Why would you be able to mine fewer than 1 time? Try again.")
    
    for i in range(iter):
        tup = generate_mine()
        await ctx.send(tup[0])
        print("Awaiting answer..." + str(tup[1]))
        msg = await bot.wait_for("message")
        print(msg.content)
        if(msg.content == str(tup[1])):
            await ctx.send("Correct! Crediting .01 BTC to your account")
            requester.credit(ctx.author.id, .01)
        else:
            await ctx.send("Wrong!")

### Gambling #################################################################################
# Gamble w/ coin flip #
@bot.command()
async def bet_flip(ctx, bet):
    """Bet BTC on a Coin Flip [bet]"""
    num = random.randrange(0,2)
    bal = requester.get_balance(ctx.author.id)
    if(float(bet) > float(bal)):
        return await ctx.send("You don't have enough BTC to do this")
    
    await ctx.send("Flipping coin...")
    
    if(num == 0):
        requester.debit(ctx.author.id, float(bet))
        await ctx.send("Tails. You Lose! Debiting account.")
        
    if(num == 1):
        requester.credit(ctx.author.id, float(bet))
        await ctx.send("Heads. You Win! Crediting account.")
        
# Play bingo #
# Place bingo bet
@bot.command()
async def bet_bingo_DEFUNCT(ctx, bet):
    bal = requester.get_balance(ctx.author.id)
    if(float(bet) > float(bal)):
        return await ctx.send("You don't have enough BTC to do this")
    strng = "You have bet "+ bet + "BTC"
    await ctx.send(strng)
    board = pb.start(bet)
    bingo = ['B ', 'I ', 'N ', 'G ', 'O ']
    await ctx.send(bingo)
    await ctx.send(board[0])
    await ctx.send(board[1])
    await ctx.send(board[2])
    await ctx.send(board[3])
    await ctx.send(board[4])
    
        
@bot.command()
async def burn(ctx, amount):
    """Burn BTC [amount]"""
    if(float(amount) <= 0):
        return await ctx.send("Cannot burn no or negative BTC")
    
    await ctx.send("Burning BTC, giving to TaxMan")
    requester.debit(ctx.author.id, float(amount))
    requester.credit(0, float(amount))
    
@bot.command()
async def TaxMan(ctx):
    """Get TaxMan's BTC holdings"""
    strng = "The TaxMan is currently worth: " + str(requester.get_balance(0))
    await ctx.send(strng)

#--Not working--#
@bot.event
async def on_member_join(self, member):
    guild = member.guild
    #if guild.system.channel is not None:
    to_send = 'Hello {0.mention} to {1.name}. If you need anything, message me'.format(member, guild)
    print("to_send")
    print("User has joined")
    await guild.system_channel.send(to_send)
        
# Annoy people who are typing #
@bot.event
#async def on_typing(channel, user, when):
async def disabled(user):
    print("Someone is typing")
    if(not user.bot):                                     # Don't respond if AleBot is typing
        str = "Hey you, {0.mention}. I see you typing".format(user)
        message = await channel.send(str)
        await asyncio.sleep(1)
        await message.delete()


### TTS ################################################################################

@bot.command()
async def speak(ctx, usr_input: str):
    """Text to Speach ["Text"]"""
    TTS.test(usr_input)
    if(ctx.voice_client):
        vc = ctx.voice_client
        query_c = 'C:\Projects\Personal\AleBot2.0\TTS/audio_cache/temp.mp3'
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query_c, executable="C:/Tools/ffmpeg/bin/ffmpeg.exe"))     # If migrating to another platform, this must be replaced
        vc.play(source, after=lambda e: print('done', e))

@bot.command()
async def speakl(ctx, usr_input: str, lang: str):
    """Text to speach + language ["Text", Language Code]"""
    TTS.test_lang(usr_input, lang)
    if(ctx.voice_client):
        vc = ctx.voice_client
        query_c = 'C:\Projects\Personal\AleBot2.0\TTS/audio_cache/temp.mp3'
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query_c, executable="C:/Tools/ffmpeg/bin/ffmpeg.exe"))     # If migrating to another platform, this must be replaced
        vc.play(source, after=lambda e: print('done', e))


### Audio ##############################################################################

## Audio Metadata ##
# Much of this audio driver is taken from Rapptz Github Repo:
# https://github.com/Rapptz/discord.py/blob/v1.7.3/examples/basic_voice.py
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable="C:/Tools/ffmpeg/bin/ffmpeg.exe"), data=data)


class add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def record(self, ctx):
        """[Not Working] Records VC audio"""
        if not ctx.message.author.voice:
            return await ctx.send("Not in VC")
    
        channel = ctx.author.voice.channel
        vc = await channel.connect()
    
        discord.AudioSource.read(self)
    
        await ctx.send("Voice recording attempted")
        
   
class fromMp3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def list_files(self, ctx):
        """Lists all audio files AleBot2.0 has saved"""
        audios = []
        for filename in os.listdir("Audio_Files"):
            audios.append(filename)
            
        await ctx.send(audios)
            
            
        
    @commands.command()
    async def play_saved(self, ctx, *, query):
        """Plays an audio file that AleBot2.0 has saved [File]"""
        if(ctx.voice_client):
            vc = ctx.voice_client
            query_c = "Audio_Files/" + query
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query_c, executable="C:/Tools/ffmpeg/bin/ffmpeg.exe"))     # If migrating to another platform, this must be replaced
            vc.play(source, after=lambda e: print('done', e))
        else:
            try:
                channel = ctx.author.voice.channel
                await channel.connect()                                 # Async bot join channel
                logger.info("AleBot2.0 has joined voice channel")
                vc = ctx.voice_client
                query_c = "Audio_Files/" + query
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query_c, executable="C:/Tools/ffmpeg/bin/ffmpeg.exe")) # If migrating to another platform, this must be replaced
                vc.play(source, after=lambda e: print('done', e))
            except:
                await ctx.send('You must be in a VC for AleBot2.0 to join')
                
    # Plays from youtube URL
    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url [URL]"""
        if(not ctx.voice_client):
            try:
                channel = ctx.author.voice.channel
                await channel.connect()                                 # Async bot join channel
                logger.info("AleBot2.0 has joined voice channel")
            except:
                await ctx.send('You must be in a VC for AleBot2.0 to join')            

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))    
    
    # Changes bot volume
    @commands.command()
    async def volume(self, ctx, volume: int):
           
        if(not ctx.voice_client):
            return await ctx.send("AleBot2.0 is not in a VC")
        if(volume < 1):
            return await ctx.send("Volume must be at least 1")
        
        ctx.voice_client.source.volume = volume / 100.0
        await ctx.send("Changed volume to {}%".format(volume))
        
    # Get bot volume
    @commands.command()
    async def get_volume(self, ctx):
        if(not ctx.voice_client):
            return await ctx.send("AleBot2.0 is not in a VC, cannot fetch volume")
        await ctx.send("Volume is: {}%".format(int(ctx.voice_client.source.volume*100)))
        
    # Stop bot playing
    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("AleBot2.0 has stopped playing")



@bot.command()
async def kill(ctx):
    await ctx.bot.logout()

### Hidden Functions ###########################################################################
@bot.command()
async def get_users(ctx):
    guild = bot.guilds
    usrs = bot.users
    #print(usrs)
    ids = []
    for usr in usrs:
        print(usr.id)
        ids.append(usr.id)
        #.encode("utf-8")
 
bot.add_cog(add(bot))
bot.add_cog(fromMp3(bot))

bot.run(get_token.get_token())  
